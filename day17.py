from heapq import heappop, heappush
from time import time

start = time()
DIRS = {0: (-1, 0), 1: (0, -1), 2: (1, 0), 3: (0, 1)}
INV_DIRS = {v: k for k, v in DIRS.items()}
recs = 0


if __name__ == "__main__":
    with open("inputs/day17.txt") as f:
        whole_input = f.read()

    grid = whole_input.split("\n")

    def min_path(inertia: int, max_elong: int) -> int:
        m = len(grid)
        n = len(grid[0])
        h = [(0, 0, 0, 1, 0), (0, 0, 0, 0, 1)]
        visited = [[[False] * n for _ in range(m)] for _ in range(4)]
        while h:
            heat_loss, i, j, di, dj = heappop(h)
            if i == m - 1 and j == n - 1:
                return heat_loss
            if visited[INV_DIRS[(di, dj)]][i][j]:
                continue
            acc_heat_l = 0
            acc_heat_r = 0
            visited[INV_DIRS[(di, dj)]][i][j] = True
            for k in range(1, max_elong + 1):
                if 0 <= i - k * dj < m and 0 <= j + k * di < n:
                    acc_heat_l += int(grid[i - k * dj][j + k * di])
                    if k >= inertia:
                        heappush(
                            h,
                            (
                                heat_loss + acc_heat_l,
                                i - k * dj,
                                j + k * di,
                                -dj,
                                di,
                            ),
                        )
                if 0 <= i + k * dj < m and 0 <= j - k * di < n:
                    acc_heat_r += int(grid[i + k * dj][j - k * di])
                    if k >= inertia:
                        heappush(
                            h,
                            (
                                heat_loss + acc_heat_r,
                                i + k * dj,
                                j - k * di,
                                dj,
                                -di,
                            ),
                        )

    print(f"    \u2022 first part: {min_path(1, 3)}")
    print(f"    \u2022 second part: {min_path(4, 10)}")

    m, s = divmod(time() - start, 60)
    print(f"Done in {m:.0f}m{s:.4f}s")
