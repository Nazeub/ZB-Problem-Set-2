# ps2.py
# Layout a Circuit Board using a CSP
# Starter Code by David Kopec
# Completed by: Zander Bueno
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


# --- Constraint Class ---
class ChipConstraint(Constraint[Chip, list[GridLocation]]):
    def __init__(self, chips: list[Chip]) -> None:
        super().__init__(chips)

    def satisfied(self, assignment: dict[Chip, list[GridLocation]]) -> bool:
        seen: set[GridLocation] = set()
        for locs in assignment.values():
            for loc in locs:
                if loc in seen:
                    return False  # overlap
                seen.add(loc)
        return True


# --- Helper: generate all possible placements for a chip ---
def generate_chip_domain(chip: Chip, rows: int, cols: int) -> list[list[GridLocation]]:
    placements: list[list[GridLocation]] = []

    orientations = {(chip.width, chip.height), (chip.height, chip.width)}  # avoid duplicates
    for (w, h) in orientations:
        if w > cols or h > rows:
            continue
        for row in range(rows - h + 1):
            for col in range(cols - w + 1):
                locs = [GridLocation(r, c) for r in range(row, row + h) for c in range(col, col + w)]
                placements.append(locs)

    return placements


def solution(chips: list[Chip], grid: Grid) -> Grid | None:
    rows, cols = len(grid), len(grid[0])

    # Build domains
    domains: dict[Chip, list[list[GridLocation]]] = {}
    for chip in chips:
        domains[chip] = generate_chip_domain(chip, rows, cols)

    # If any chip has no valid placements, early return
    if any(len(domain) == 0 for domain in domains.values()):
        return None

    # Create CSP
    csp: CSP[Chip, list[GridLocation]] = CSP(chips, domains)
    csp.add_constraint(ChipConstraint(chips))

    # Solve
    result = csp.backtracking_search()
    if result is None:
        return None

    # Copy the grid and fill in chips
    final_grid = [row[:] for row in grid]
    for chip, locations in result.items():
        for loc in locations:
            final_grid[loc.row][loc.column] = chip.symbol

    return final_grid


if __name__ == "__main__":
    easy_grid = generate_grid(10, 10)
    easy_chips = [Chip(5, 5, "*"), Chip(4, 4, "#"), Chip(2, 2, "@")]
    sol = solution(easy_chips, easy_grid)
    if sol is None:
        print("No solution found!")
    else:
        display_grid(sol)
