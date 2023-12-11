from time import time
from collections import deque

if __name__ == "__main__":

    def vect(v1, v2):
        return v1[0] * v2[1] - v1[1] * v2[0]

    def rot(left: bool, v):
        return -(2 * int(left) - 1) * v[1], (2 * int(left) - 1) * v[0]

    start = time()
    with open("inputs/day10.txt", "r") as f:
        lines = f.readlines()
    m = len(lines[0]) + 1
    grid = (
        ["." * m]
        + ["." + line[:-1] + "." for line in lines[:-1]]
        + ["." + lines[-1] + "."]
        + ["." * m]
    )
    n = len(grid)
    N = (-1, 0)
    S = (1, 0)
    W = (0, -1)
    E = (0, 1)
    chars = {
        "|": {N, S},
        "-": {E, W},
        "L": {N, E},
        "J": {N, W},
        "7": {S, W},
        "F": {S, E},
    }
    inv_chars = {tuple(v): k for k, v in chars.items()}
    for i, line in enumerate(grid):
        if line.find("S") >= 0:
            i0, j0 = i, line.find("S")
            for start_, end in [(N, S), (N, W), (N, E), (E, W), (E, S), (W, S)]:
                dil, djl = end
                di1, dj1 = start_
                if (-dil, -djl) in chars[grid[i0 + dil][j0 + djl]] and (
                    -di1,
                    -dj1,
                ) in chars[grid[i0 + di1][j0 + dj1]]:
                    new_char = inv_chars.get((end, start_), inv_chars[(start_, end)])
                    grid[i0] = grid[i0][:j0] + new_char + grid[i0][j0 + 1 :]
                    break
            break
    loop = {}
    turns_right = 0
    turns_left = 0
    prev = i0, j0
    ptr = i0 + di1, j0 + dj1
    
    while ptr not in loop:
        dir_from = prev[0] - ptr[0], prev[1] - ptr[1]
        dir_to = (chars[grid[ptr[0]][ptr[1]]] - {dir_from}).pop()
        z = vect(dir_from, dir_to)
        turns_right += int(z == 1)
        turns_left += int(z == -1)
        loop[ptr] = dir_to, dir_from, -z
        prev = ptr
        ptr = ptr[0] + dir_to[0], ptr[1] + dir_to[1]

    seen = [[False] * m for _ in range(n)]
    left = turns_left > turns_right
    area = 0
    
    q = deque()
    
    for i, j in loop:
        seen[i][j] = True
    
    for i, j in loop:
        dir_to, dir_from, turn = loop[(i, j)]
        if turn == 2 * int(left) - 1:
            neighbors = [(i + dir_to[0] + dir_from[0], j + dir_to[1] + dir_from[1])]
        elif turn == -2 * int(left) + 1:
            neighbors = [
                (i - dir_to[0] - dir_from[0], j - dir_to[1] - dir_from[1]),
                (i, j - dir_to[1] - dir_from[1]),
                (i - dir_to[0] - dir_from[0], j),
            ]
        else:
            di, dj = rot(left, dir_to)
            neighbors = [(i + di, j + dj)]
        for ii, jj in neighbors:
            if not seen[ii][jj]:
                q.append((ii, jj))
                seen[ii][jj] = True
            while q:
                x, y = q.popleft()
                area += 1
                for di, dj in [N, S, E, W]:
                    xx, yy = x + di, y + dj
                    if not seen[xx][yy]:
                        q.append((xx, yy))
                        seen[xx][yy] = True

    m, s = divmod(time() - start, 60)

    print(f"    \u2022 first part: {len(loop) // 2}")
    print(f"    \u2022 second part: {area}")
    print(f"Done in {m:.0f}m{s:.4f}s")
