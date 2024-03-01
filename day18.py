import re
from collections import deque
from itertools import pairwise
from time import time


def vect(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]


def rot(left: bool, v):
    return -(2 * int(left) - 1) * v[1], (2 * int(left) - 1) * v[0]


DIRS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
NUM_DIRS = {"0": "R", "1": "D", "2": "L", "3": "U"}


if __name__ == "__main__":
    start = time()
    with open("inputs/day18.txt", "r") as f:
        lines = f.readlines()
    last_stop_this_train = lines[-1]
    turns_right = 0
    turns_left = 0
    loop = []
    prev_dir, _, _ = last_stop_this_train.split(" ")
    i, j = 0, 0
    for line in lines:
        dir_, steps, col = line.split(" ")
        di, dj = DIRS[dir_]
        loop.append((i, j, prev_dir, dir_))
        if prev_dir:
            if vect(DIRS[prev_dir], (di, dj)) == 1:
                turns_left += 1
            else:
                turns_right += 1
        prev_dir = dir_
        for k in range(1, int(steps)):
            loop.append((i + k * di, j + k * dj, dir_, dir_))
        i, j = i + int(steps) * di, j + int(steps) * dj

    i1 = max(i for i, _, _, _ in loop)
    j1 = max(j for _, j, _, _ in loop)
    i0 = min(i for i, _, _, _ in loop)
    j0 = min(j for _, j, _, _ in loop)
    n = j1 - j0 + 1
    m = i1 - i0 + 1
    grid = [["."] * n for _ in range(m)]

    seen = [[False] * n for _ in range(m)]
    for k, l, _, _ in loop:
        grid[k - i0][l - j0] = "#"
        seen[k - i0][l - j0] = True

    q = deque()
    left = turns_left > turns_right
    area = 0
    for i, j, prev_dir, dir_ in loop:
        turn = -vect(DIRS[prev_dir], DIRS[dir_])
        di, dj = DIRS[prev_dir]
        dii, djj = DIRS[dir_]
        if turn == -2 * int(left) + 1:
            neighbors = [(i - di + dii, j - dj + djj)]
        elif turn == 2 * int(left) - 1:
            neighbors = [
                (i + di - dii, j + dj - djj),
                (i, j - djj - djj),
                (i - di - dii, j),
            ]
        else:
            di, dj = rot(left, DIRS[dir_])
            neighbors = [(i + di, j + dj)]
        for ii, jj in neighbors:
            if not seen[ii - i0][jj - j0]:
                q.append((ii, jj))
                seen[ii - i0][jj - j0] = True
            while q:
                x, y = q.popleft()
                area += 1
                for di, dj in DIRS.values():
                    xx, yy = x + di, y + dj
                    if not seen[xx - i0][yy - j0]:
                        q.append((xx, yy))
                        seen[xx - i0][yy - j0] = True

    i, j = 0, 0
    prev_dir = DIRS[NUM_DIRS[re.search(r"[0-3](?=\)$)", lines[-1]).group()]]
    coordinates = []
    for line in lines:
        hex_ = re.search(r"(?<=#)[a-f0-9]{5}", line).group()
        dir_ = re.search(r"[0-3](?=\)$)", line).group()
        steps = int(hex_, 16)
        dii, djj = prev_dir
        di, dj = DIRS[NUM_DIRS[dir_]]
        turn = vect((dii, djj), (di, dj))
        if turn == -1:
            coordinates.append((i + 0.5 * dii - 0.5 * di, j + 0.5 * djj - 0.5 * dj))
        elif turn == +1:
            coordinates.append((i - 0.5 * dii + 0.5 * di, j - 0.5 * djj + 0.5 * dj))
        i += steps * di
        j += steps * dj
        prev_dir = di, dj

    coordinates.append(coordinates[0])
    ans2 = 0

    for (x1, y1), (x2, y2) in pairwise(coordinates):
        ans2 += (y1 + y2) * (x2 - x1)

    print(f"    \u2022 first part: {area + len(loop)}")
    print(f"    \u2022 second part: {ans2 / 2}")
    # print(f"    \u2022 second part: {area}")
    m, s = divmod(time() - start, 60)
    print(f"Done in {m:.0f}m{s:.4f}s")
