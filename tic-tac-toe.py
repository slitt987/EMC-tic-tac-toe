"""A tic-tac-toe game built with Python and Tkinter."""

from lib import *
from itertools import cycle
from pprint import pprint


def main():
    """Create the game's board and run its main loop."""
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()