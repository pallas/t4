import pytest
import ttkbootstrap as ttk
from t4.__main__ import (
    Board,
    Cell,
    Mark,
    State,
    )

@pytest.fixture
def app():
    root = ttk.Window()
    root.withdraw()
    yield root
    root.destroy()

def test_board_reset(app):
    board = Board(app)
    board.reset()
    assert all(
        cell.mark == Mark.EMPTY
        for cell in board.cells.values()
    )

def test_board_no_winner(app):
    board = Board(app)
    layouts = (
        ("   ",
         " XO",
         "XO ",),

        ("X X",
         "O O",
         " X ",),

        ("XOX",
         "OO ",
         "X X",),

        )
    for layout in layouts:
        board.reset()
        board.load(layout)
        assert board.winner() is None, board.export_str()

def test_board_x_wins(app):
    board = Board(app)
    layouts = (
        ("XXX",
         "   ",
         "   ",),

        ("   ",
         "XXX",
         "   ",),

        ("   ",
         "   ",
         "XXX",),

        ("X  ",
         "X  ",
         "X  ",),

        (" X ",
         " X ",
         " X ",),

        ("  X",
         "  X",
         "  X",),

        ("  X",
         " X ",
         "X  ",),

        ("X  ",
         " X ",
         "  X",),
    )
    for layout in layouts:
        board.reset()
        board.load(layout)
        assert board.winner() is Mark.X, board.export_str()

def test_board_o_wins(app):
    board = Board(app)
    layouts = (
        ("OOO",
         "   ",
         "   ",),

        ("   ",
         "OOO",
         "   ",),

        ("   ",
         "   ",
         "OOO",),

        ("O  ",
         "O  ",
         "O  ",),

        (" O ",
         " O ",
         " O ",),

        ("  O",
         "  O",
         "  O",),

        ("  O",
         " O ",
         "O  ",),

        ("O  ",
         " O ",
         "  O",),
    )
    for layout in layouts:
        board.reset()
        board.load(layout)
        assert board.winner() is Mark.O, board.export_str()

def test_board_cats_game(app):
    board = Board(app)
    layouts = (
        ("OXO",
         "OXX",
         "XOX",),
        )
    for layout in layouts:
        board.reset()
        board.load(layout)
        assert board.winner() is Mark.EMPTY, board.export_str()
