from itertools import cycle
from .TicTacToeBoard import *
from pprint import pprint
import math

BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="green"),
)

class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self._players_list = players
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()
        self._number_of_players=2

    def set_number_of_players(self, number_of_players):
        self._number_of_players=number_of_players

    def is_single_player(self):
        return self._number_of_players == 1

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        """Return a list of all combinations of winning moves. (List of Lists)"""
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]
    
    def toggle_player(self):
        """Return a toggled player."""
        self.current_player = next(self._players)

    def is_valid_move(self, move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self, move):
        """Process the current move and check if it's a win."""
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        for combo in self._winning_combos:
            results = set(self._current_moves[n][m].label for n, m in combo)
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner

    def is_tied(self):
        """Return True if the game is tied, and False otherwise."""
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)
    
    def game_over(self):
        """Return True if the game is over, and False otherwise."""
        return self._has_winner or self.is_tied()

    def reset_game(self):
        """Reset the game state to play again."""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []

    def get_computer_next_move(self):
        move = self.block_move(self.board_size-1)
        if move is None:
            move = self.get_center_space()
            if move is None:
                if self.check_opponent_center_space():
                    move = self.get_corner_next()
                else:
                    move = self.get_not_corner_next()
                if move is None:
                    move = self.next_open_spot()

        return move
    
    def _get_opponent(self):
        """Return the opponent of the current player."""
        return [player.label for player in self._players_list if player.label != self.current_player.label][0]

    def block_move(self, block_length):
        opponent = self._get_opponent()

        for combo in self._winning_combos:
            possible = [self._current_moves[n][m] for n, m in combo]
            blocks = [move for move in possible if move.label == ""]
            opponent_moves = [move for move in possible if move.label == opponent]
            # Check if there is an opponent move the right length and that all remaining moves are empty (needing
            # a block). This allows for handling of a block length of 2 on a 4x4 board then only being needed
            # if there are 2 open moves
            if len(opponent_moves) == block_length and len(blocks) == self.board_size - block_length:
                block = blocks[0]
                return Move(block.row, block.col, self.current_player.label)

        return None
    
    def check_opponent_center_space(self):
        if self.board_size % 2 == 0:
            return False
        
        center = math.floor(self.board_size / 2)
        if self._current_moves[center][center].label not in ["", self.current_player.label]:
            return True
        
        return False

    def get_center_space(self):
        if self.board_size % 2 == 0:
            return None
        
        center = math.floor(self.board_size / 2)
        if self._current_moves[center][center].label == "":
            return Move(center, center, self.current_player.label)

        return None
    
    def get_not_corner_next(self):
        edge = self.board_size - 1
        moves = [(m.row, m.col) 
                 for row in self._current_moves 
                 for m in row 
                 if m.label == '' and (m.row, m.col) not in [(0,0),(0,edge),(edge,0),(edge,edge)]]
        
        if len(moves) == 0:
            return None
        else:
            (row, col) = moves[0]
            move = Move(row, col, self.current_player.label)
            return move
        
    def get_corner_next(self):
        edge = self.board_size - 1
        moves = [(m.row, m.col) 
                 for row in self._current_moves 
                 for m in row 
                 if m.label == '' and (m.row, m.col) in [(0,0),(0,edge),(edge,0),(edge,edge)]]
        
        if len(moves) == 0:
            return None
        else:
            (row, col) = moves[0]
            move = Move(row, col, self.current_player.label)
            return move

    def next_open_spot(self):
        """Return the next available move on the board."""
        
        (row, col) = [(m.row, m.col) for row in self._current_moves for m in row if m.label == ''][0]
        move = Move(row, col, self.current_player.label)
        return move
