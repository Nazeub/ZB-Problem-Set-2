# ps2.py
# Layout a Circuit Board using a CSP
# Starter Code by David Kopec
# Completed by: [your name here]
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
    return [["-" for _ in range(columns)] for _ in range(rows)]

def display_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))

class ChipConstraint(Constraint[Chip, tuple[list[GridLocation], tuple[int, int]]]):
    def __init__(self, chips: list[Chip]) -> None:
        super().__init__(chips)
        self.chips = chips

    def satisfied(self, assignment: dict[Chip, tuple[list[GridLocation], tuple[int, int]]]) -> bool:
        all_locs: set[GridLocation] = set()
        for placement in assignment.values():
            locations = placement[0]
            for loc in locations:
                if loc in all_locs:
                    return False  # overlap
                all_locs.add(loc)
        return True

def generate_chip_domain(chip: Chip, rows: int, cols: int) -> list[tuple[list[GridLocation], tuple[int, int]]]:
    placements: list[tuple[list[GridLocation], tuple[int, int]]] = []

    # Try both orientations: (width, height) and (height, width)
    for (w, h) in [(chip.width, chip.height), (chip.height, chip.width)]:
        # Only add unique placements if w==h (square), to avoid duplicates
        if chip.width == chip.height and (w, h) != (chip.width, chip.height):
            continue
        for row in range(rows - h + 1):
            for col in range(cols - w + 1):
                locs: list[GridLocation] = []
                for r in range(row, row + h):
                    for c in range(col, col + w):
                        locs.append(GridLocation(r, c))
                placements.append((locs, (w, h)))
    return placements

def solution(chips: list[Chip], grid: Grid) -> Grid | None:
    rows, cols = len(grid), len(grid[0])

    # Build domains
    domains: dict[Chip, list[tuple[list[GridLocation], tuple[int, int]]]] = {}
    for chip in chips:
        domains[chip] = generate_chip_domain(chip, rows, cols)

    # Create CSP
    csp: CSP[Chip, tuple[list[GridLocation], tuple[int, int]]] = CSP(chips, domains)
    csp.add_constraint(ChipConstraint(chips))

    # Solve
    result = csp.backtracking_search()
    if result is None:
        return None

    # Fill in grid with solution
    for chip, placement in result.items():
        locations = placement[0]
        for loc in locations:
            grid[loc.row][loc.column] = chip.symbol

    return grid

if __name__ == "__main__":
    easy_grid = generate_grid(10, 10)
    easy_chips = [Chip(5, 5, "*"), Chip(4, 4, "#"), Chip(2, 2, "@")]
    sol = solution(easy_chips, easy_grid)
    if sol is None:
        print("No solution found!")
    else:
        display_grid(sol)
