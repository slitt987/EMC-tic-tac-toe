import tkinter as tk
from tkinter import font
from typing import NamedTuple
from pprint import pprint

class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        players_menu = tk.Menu(master=menu_bar)
        players_menu.add_command(label="Single Player", command=self._single_player)
        players_menu.add_command(label="Two Player", command=self._two_player)
        menu_bar.add_cascade(label="Players", menu=players_menu)

    def _single_player(self):
        self.reset_board()
        self._game.set_number_of_players(1)

    def _two_player(self):
        self.reset_board()
        self._game.set_number_of_players(2)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")
    
    def _get_button(self, coordinates):
        for button, button_coordinates in self._cells.items():
            if button_coordinates == coordinates:
                return button

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")

    def check_board(self):
        """Check the status of the board after tha last move to see if the game is over, or switch to the next players turn"""
        if self._game.is_tied():
            self._update_display(msg="Tied game!", color="red")
        elif self._game.has_winner():
            self._highlight_cells()
            msg = f'Player "{self._game.current_player.label}" won!'
            color = self._game.current_player.color
            self._update_display(msg, color)
        else:
            self._game.toggle_player()
            msg = f"{self._game.current_player.label}'s turn"
            self._update_display(msg)

    def play(self, event):
        """Handle a player's move."""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)

        if self._game.is_valid_move(move):
             self.user_play(clicked_btn, move)

        if self._game.is_single_player() and not self._game.game_over():
             self.computer_play()

    def user_play(self, clicked_btn, move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            self.check_board()

    def computer_play(self):
            """Process a move for the computer player"""
            move = self._game.get_computer_next_move()
            button = self._get_button((move.row, move.col))
            self._update_button(button)
            self._game.process_move(move)
            self.check_board()
