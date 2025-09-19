# ps2.py
# Layout a Circuit Board using a CSP
# Starter Code by David Kopec
# Completed by: Ivan Rivera
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


# YOUR CODE HERE Used Copilot, Google and Chatgpt for help and correct syntax 

class ChipConstraint(Constraint[Chip, tuple[int, int, bool]]):
    """
    A constraint ensuring chips do not overlap.
    Assignment maps Chip -> (row, col, rotated).
    """
    def __init__(self, chips: list[Chip]) -> None:
        super().__init__(chips)
        self.chips = chips

    def satisfied(self, assignment: dict[Chip, tuple[int, int, bool]]) -> bool:
        occupied: set[tuple[int, int]] = set()
        for chip, (row, col, rotated) in assignment.items():
            w, h = (chip.height, chip.width) if rotated else (chip.width, chip.height)
            for r in range(h):
                for c in range(w):
                    pos = (row + r, col + c)
                    if pos in occupied:
                        return False  # overlap detected
                    occupied.add(pos)
        return True


def generate_domains(chips: list[Chip], grid: Grid) -> dict[Chip, list[tuple[int, int, bool]]]:
    rows, cols = len(grid), len(grid[0])
    domains: dict[Chip, list[tuple[int, int, bool]]] = {}
    for chip in chips:
        positions: list[tuple[int, int, bool]] = []
        # normal orientation
        for r in range(rows - chip.height + 1):
            for c in range(cols - chip.width + 1):
                positions.append((r, c, False))
        # rotated orientation (if different)
        if chip.width != chip.height:
            for r in range(rows - chip.width + 1):
                for c in range(cols - chip.height + 1):
                    positions.append((r, c, True))
        domains[chip] = positions
    return domains


def fill_grid(grid: Grid, assignment: dict[Chip, tuple[int, int, bool]]) -> Grid:
    new_grid = [row[:] for row in grid]  # copy grid
    for chip, (row, col, rotated) in assignment.items():
        w, h = (chip.height, chip.width) if rotated else (chip.width, chip.height)
        for r in range(h):
            for c in range(w):
                new_grid[row + r][col + c] = chip.symbol
    return new_grid


def solution(chips: list[Chip], grid: Grid) -> Grid | None:
    
# Find a way to fit all of the chips onto the board and return a filled-in grid. If the chips can't fit, return None.
# YOUR CODE HERE 
    domains = generate_domains(chips, grid)
    csp = CSP(chips, domains)
    csp.add_constraint(ChipConstraint(chips))
    assignment = csp.backtracking_search()
    if assignment is None:
        return None
    return fill_grid(grid, assignment)



if __name__ == "__main__":
    easy_grid = generate_grid(10, 10)
    easy_chips = [Chip(5, 5, "*"), Chip(4, 4, "#"), Chip(2, 2, "@")]
    sol = solution(easy_chips, easy_grid)
    if sol is None:
        print("No solution found!")
    else:
        display_grid(sol)
