from copy import deepcopy
from itertools import product
from time import time

start = time()

def slide(i0, j0, grid, dir):
    i, j = i0, j0
    di, dj = dir
    m, n = len(grid), len(grid[0])
    rock = grid[i0][j0]
    while 0 <= i + di < m and 0 <= j + dj < n and grid[i + di][j + dj] == ".":
        i += di
        j += dj
    grid[i0][j0] = "."
    grid[i][j] = rock

def load(dir, grid):
    di, dj = dir
    m, n = len(grid), len(grid[0])
    rock_indices = [(i, j) for i, j in product(range(m), range(n)) if grid[i][j] == "O"]
    if di == 1:
        return sum(1 + i for (i, _) in rock_indices)
    if di == -1:
        return sum(m - i for (i, _) in rock_indices)
    if dj == 1:
        return sum(1 + j for (_, j) in rock_indices)
    if dj == - 1:
        return sum(n - j for (_, j) in rock_indices)


def tilt(dir, grid):
    dx, dy = dir
    m, n = len(grid), len(grid[0])
    row_indices = list(range(m))
    col_indices = list(range(n))
    if dx == 1:
        row_indices = row_indices[::-1]
    if dy == 1:
        col_indices = col_indices[::-1]
    for i in row_indices:
        for j in col_indices:
            if grid[i][j] == "O":
                slide(i, j, grid, dir)


if __name__ == "__main__":
    with open("inputs/day14.txt") as f:
        whole_input = f.read()
    rows = whole_input.split("\n")
    grid = [list(row) for row in rows]
    
    N = (-1, 0)
    S = (1, 0)
    E = (0, 1)
    W = (0, -1)
    BIG_NUMBER = 1_000_000_000
    
    grid_ref = deepcopy(grid)
    tilt(N, grid)
    print(f"    \u2022 first part: {load(N, grid)}")
    
    cycle = [N, W, S, E]
    n_cycles = 0
    grid = grid_ref

    past_grids = {}
    grid_snap = ""    
    
    while grid_snap not in past_grids:
        past_grids[grid_snap] = n_cycles
        for dir in cycle:
            tilt(dir, grid)
        grid_snap = "\n".join("".join(line) for line in grid)
        n_cycles += 1

    len_cycle = n_cycles - past_grids[grid_snap]
    steps_start = past_grids[grid_snap]
    value = ((BIG_NUMBER - steps_start) % len_cycle) + steps_start
    grid_final = ""
    for k, v in past_grids.items():
        if v == value:
            grid_final = k
            break
    load_ = load(N, [list(row) for row in grid_final.split('\n')])
    
    m, s = divmod(time() - start, 60)
    print(f"    \u2022 second part: {load_}")
    print(f"Done in {m:.0f}m{s:.4f}s")
