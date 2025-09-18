# ps2.py
# Layout a Circuit Board using a CSP
# Starter Code by David Kopec
# Completed by:
from __future__ import annotations
from csp import CSP, Constraint
from typing import NamedTuple


Grid = list[list[str]]  # type alias for grids


class GridLocation(NamedTuple):
    row: int
    column: int


class Chip(NamedTuple):
    width: int
    height: int
    symbol: str


def generate_grid(rows: int, columns: int) -> Grid:
    # initialize grid with random letters
    return [["-" for c in range(columns)] for r in range(rows)]


def display_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))


# YOUR CODE HERE


def solution(chips: list[Chip], grid: Grid) -> Grid | None:
    """
    Find a way to fit all of the chips onto the board and return 
    a filled-in grid. If the chips can't fit, return None.
    """
    # YOUR CODE HERE


if __name__ == "__main__":
    easy_grid = generate_grid(10, 10)
    easy_chips = [Chip(5, 5, "*"), Chip(4, 4, "#"), Chip(2, 2, "@")]
    sol = solution(easy_chips, easy_grid)
    if sol is None:
        print("No solution found!")
    else:
        display_grid(sol)
