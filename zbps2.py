# ps2.py
# Layout a Circuit Board using a CSP
# Starter Code by David Kopec
# Completed by: [Your Name] (Cite sources below)
from __future__ import annotations
from csp import CSP, Constraint
from typing import NamedTuple, Tuple, Dict, List, Optional

Grid = list[list[str]]  # type alias for grids

class GridLocation(NamedTuple):
    row: int
    column: int

class Chip(NamedTuple):
    width: int
    height: int
    symbol: str

def generate_grid(rows: int, columns: int) -> Grid:
    # initialize grid with blank
    return [["-" for c in range(columns)] for r in range(rows)]

def display_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))

def get_possible_placements(chip: Chip, grid: Grid) -> List[Tuple[int, int, int, int]]:
    """Generate all possible placements for this chip on the grid, including rotations.
    Each placement is (row, col, width, height), representing the top-left corner and orientation."""
    placements = []
    rows, cols = len(grid), len(grid[0])
    for w, h in [(chip.width, chip.height), (chip.height, chip.width)] if chip.width != chip.height else [(chip.width, chip.height)]:
        for r in range(rows - h + 1):
            for c in range(cols - w + 1):
                placements.append((r, c, w, h))
    return placements

def rectangles_overlap(a: Tuple[int, int, int, int], b: Tuple[int, int, int, int]) -> bool:
    """Check if two rectangles overlap. Rectangle: (row, col, width, height)"""
    ar, ac, aw, ah = a
    br, bc, bw, bh = b
    # If one rectangle is to the left/right/top/bottom of the other, they don't overlap
    if ac + aw <= bc or bc + bw <= ac:
        return False
    if ar + ah <= br or br + bh <= ar:
        return False
    return True

class ChipPlacementConstraint(Constraint[Chip, Tuple[int, int, int, int]]):
    """Constraint that ensures no chips overlap."""
    def __init__(self, chips: List[Chip]):
        super().__init__(chips)

    def satisfied(self, assignment: Dict[Chip, Tuple[int, int, int, int]]) -> bool:
        # For every pair of chips with assigned placements, check they don't overlap
        items = list(assignment.items())
        for i in range(len(items)):
            chip_a, place_a = items[i]
            for j in range(i+1, len(items)):
                chip_b, place_b = items[j]
                if rectangles_overlap(place_a, place_b):
                    return False
        return True

def solution(chips: list[Chip], grid: Grid) -> Grid | None:
    """Find a way to fit all of the chips onto the board and return a filled-in grid. If the chips can't fit, return None."""
    # Generate domains for each chip: all possible placements (with rotation)
    domains: Dict[Chip, List[Tuple[int, int, int, int]]] = {}
    for chip in chips:
        domains[chip] = get_possible_placements(chip, grid)

    # Setup CSP
    csp = CSP(chips, domains)
    csp.add_constraint(ChipPlacementConstraint(chips))

    # Solve
    result = csp.backtracking_search()
    if result is None:
        return None

    # Fill grid
    filled_grid = [row[:] for row in grid]  # copy
    for chip, (r, c, w, h) in result.items():
        for dr in range(h):
            for dc in range(w):
                filled_grid[r + dr][c + dc] = chip.symbol
    return filled_grid

# Cite sources:
# - Inspired by word search code from Classic Computer Science Problems in Python, Chapter 3

if __name__ == "__main__":
    easy_grid = generate_grid(10, 10)
    easy_chips = [Chip(5, 5, "*"), Chip(4, 4, "#"), Chip(2, 2, "@")]
    sol = solution(easy_chips, easy_grid)
    if sol is None:
        print("No solution found!")
    else:
        display_grid(sol)
