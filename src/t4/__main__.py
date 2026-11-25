# SPDX-License-Identifier: MIT
# Author: Derrick Lyndon Pallas <derrick@pallas.us>
import ttkbootstrap as ttk
from loguru import logger as log
from typing import NamedTuple
from enum import Enum, auto
from collections import defaultdict, Counter
from dataclasses import dataclass, field
from itertools import product, repeat

class MarkStyle(NamedTuple):
    text: str

class Mark(Enum):
    EMPTY = MarkStyle(text=" ")
    X = MarkStyle(text="𝓧")
    O = MarkStyle(text="𝓞")

class StateStyle(NamedTuple):
    text: str

class State(Enum):
    X_TURN = StateStyle(text="X's turn")
    O_TURN = StateStyle(text="O's turn")
    X_WINS = StateStyle(text="X wins!")
    O_WINS = StateStyle(text="O wins!")
    NOBODY = StateStyle(text="🐈‍⬛")

@dataclass(slots=True)
class Cell(ttk.Button):
    board: Board
    row: int
    col: int
    _mark: Mark

    def __init__(self, board: Board, row: int, col: int):
        super().__init__(
            board,
            width=5,
            bootstyle="outline",
            command=lambda: self.on_click(),
        )

        self.board = board
        self.row = row
        self.col = col

    @property
    def id(self) -> tuple(int, int):
        return (self.row, self.col)

    def on_click(self) -> None:
        log.info(f"{self.id}")
        self.board.game.pick_cell(self)

    @property
    def mark(self) -> Mark:
        return self._mark

    @mark.setter
    def mark(self, value: Mark) -> None:
        self._mark = value
        self.configure(text=self._mark.value.text)

@dataclass(slots=True)
class Board(ttk.Frame):
    game: Game
    rows: int
    columns: int
    cells: dict[(int, int), Cell] = field(default_factory=lambda: defaultdict(Cell))

    def __init__(self, parent, rows=3, columns=3):
        super().__init__(parent, padding=20)

        self.game = parent
        self.rows = rows
        self.columns = columns

        self.cells = {}
        for r, c in product(range(self.rows), range(self.columns)):
            cell = Cell(self, r, c)
            self.cells[(r,c)] = cell
            cell.grid(row=r, column=c, padx=2, pady=2, ipady=20)

    def histogram(self, ids) -> dict[Mark, int]:
        cells = map(lambda id: self.cells[id], ids)
        return Counter(cell.mark for cell in cells)

    def winner(self) -> Mark:
        for r in range(self.rows):
            ids = zip(repeat(r), range(self.columns))
            cells = [self.cells[id] for id in ids]
            counts = Counter(cell.mark for cell in cells)
            for mark in (Mark.X, Mark.O):
                if counts[mark] == len(cells):
                    return mark

        for c in range(self.columns):
            ids = zip(range(self.rows), repeat(c))
            cells = [self.cells[id] for id in ids]
            counts = Counter(cell.mark for cell in cells)
            for mark in (Mark.X, Mark.O):
                if counts[mark] == len(cells):
                    return mark

        if self.rows == self.columns:
            ids = zip(range(self.rows), range(self.columns))
            cells = [self.cells[id] for id in ids]
            counts = Counter(cell.mark for cell in cells)
            for mark in (Mark.X, Mark.O):
                if counts[mark] == len(cells):
                    return mark

            ids = zip(range(self.rows), reversed(range(self.columns)))
            cells = [self.cells[id] for id in ids]
            counts = Counter(cell.mark for cell in cells)
            for mark in (Mark.X, Mark.O):
                if counts[mark] == len(cells):
                    return mark

        cells = self.cells.values()
        if not sum(cell.mark == Mark.EMPTY for cell in cells):
            return Mark.EMPTY

    def reset(self):
        for cell in self.cells.values():
            cell.mark = Mark.EMPTY

@dataclass(slots=True)
class Game(ttk.Canvas):
    board: Board
    _state: State
    status: ttk.Label
    button: ttk.Button

    def __init__(self, parent):
        super().__init__(parent, width=300, height=300)
        self.board = Board(self)
        self.status = ttk.Label(self)
        self.button = ttk.Button(
            parent,
            text="Reset?",
            command=self.reset,
            )
        self.reset()

    def pack(self, *args, **kwargs):
        self.board.pack()
        self.status.pack()
        self.button.pack(side="bottom")
        super().pack(*args, **kwargs)

    def reset(self) -> None:
        self.state = State.X_TURN
        self.board.reset()

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, value: State) -> None:
        self._state = value
        self.status.configure(text=self._state.value.text)

    def pick_cell(self, cell) -> None:
        if cell.mark != Mark.EMPTY:
            log.info(f"cell {cell.id} already taken by {cell.mark.value.text}")
        else:
            match self.state:
                case State.X_TURN:
                    cell.mark = Mark.X
                    self.state = State.O_TURN

                case State.O_TURN:
                    cell.mark = Mark.O
                    self.state = State.X_TURN

        match self.board.winner():
            case Mark.X:
                self.state = State.X_WINS

            case Mark.O:
                self.state = State.O_WINS

            case Mark.EMPTY:
                self.state = State.NOBODY

def main() -> None:
    app = ttk.Window(title="Tic Tac Toe")
    game = Game(app).pack()
    app.mainloop()

if __name__ == "__main__":
    main()
