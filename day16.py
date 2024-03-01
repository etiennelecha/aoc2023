from functools import lru_cache, reduce
from itertools import product
from time import time

start = time()
DIRS = {0: (-1, 0), 1: (0, -1), 2: (1, 0), 3: (0, 1)}
INV_DIRS = {v: k for k, v in DIRS.items()}


def step(beam):
    ans = []
    i, j, dir = beam
    di, dj = DIRS[dir]
    if grid[i][j] == "|" and di == 0:
        ans.append((i + 1, j, 2))
        ans.append((i - 1, j, 0))
    elif grid[i][j] == "-" and dj == 0:
        ans.append((i, j + 1, 3))
        ans.append((i, j - 1, 1))
    elif grid[i][j] == "/":
        di, dj = -dj, -di
        ans.append((i + di, j + dj, INV_DIRS[(di, dj)]))
    elif grid[i][j] == "\\":
        di, dj = dj, di
        ans.append((i + di, j + dj, INV_DIRS[(di, dj)]))
    else:
        ans.append((i + di, j + dj, dir))
    return list(
        filter(
            lambda t: 0 <= t[0] < m
            and 0 <= t[1] < n
            and not explored[t[2]][t[0]][t[1]],
            ans,
        )
    )


if __name__ == "__main__":
    with open("inputs/day16.txt") as f:
        whole_input = f.read()
    rows = whole_input.split("\n")
    grid = [list(row) for row in rows]
    m = len(grid)
    n = len(grid[0])
    ans2 = 0
    for i0, j0, dir0 in (
        [(0, j, 2) for j in range(n)]
        + [(m - 1, j, 0) for j in range(n)]
        + [(i, 0, 3) for i in range(m)]
        + [(i, n - 1, 1) for i in range(m)]
    ):
        explored = [[[False] * n for _ in range(m)] for _ in range(4)]
        curr = [(i0, j0, dir0)]
        explored[dir0][i0][j0] = True
        i = 0
        steps = 0
        while curr:
            curr = reduce(lambda a, b: a + b, map(step, curr))
            for i, j, dir in curr:
                #if not explored[dir][i][j]:
                explored[dir][i][j] = True

        lit = len(
            [
                (i, j)
                for i, j in product(range(m), range(n))
                if any(explored[dir][i][j] for dir in (0, 1, 2, 3))
            ]
        )
        ans2 = max(lit, ans2)

    m, s = divmod(time() - start, 60)
    print(ans2)
    print(f"Done in {m:.0f}m{s:.4f}s")
