from collections import deque
from time import time

N_STEPS = 26501365
N = -1, 0
SUD = 1, 0
E = 0, 1
W = 0, -1

if __name__ == "__main__":
    start = time()
    with open("inputs/day21.txt") as f:
        whole_input = f.read()

    grid = whole_input.split("\n")
    m = len(grid)
    n = len(grid[0])

    def n_spots(steps):
        q = deque()
        S = 65, 65
        q.append(S)
        seen = {}
        seen[S] = 0
        n_steps = 0
        while q and n_steps < steps:
            l = len(q)
            for _ in range(l):
                i, j = q.popleft()
                for di, dj in [N, SUD, E, W]:
                    ii, jj = i + di, j + dj
                    if grid[ii % m][jj % n] != "#" and (ii, jj) not in seen:
                        q.append((ii, jj))
                        seen[(ii, jj)] = (n_steps + 1) % 2
            n_steps += 1

        return len([(i, j) for i, j in seen if seen[(i, j)] == steps % 2])

    interpolates = list(map(n_spots, [65, 131 + 65, 2 * 131 + 65]))
    print(interpolates)

    n_cards = N_STEPS // 131

    b0 = interpolates[0]
    b1 = interpolates[1] - interpolates[0]
    b2 = interpolates[2] - interpolates[1]
    f = lambda n: b0 + b1 * n + n * (n - 1) // 2 * (b2 - b1)
    print(f"    \u2022 second part: {f(N_STEPS // 131)}")
    m, s = divmod(time() - start, 60)
    print(f"Done in {m:.0f}m{s:.4f}s")