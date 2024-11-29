import sys
from collections import defaultdict, deque
from time import time

start = time()
DIRS = [(-1, 0), (0, -1), (1, 0), (0, 1)]
CHEVRONS = {"<": (0, -1), ">": (0, 1), "v": (1, 0), "^": (-1, 0)}
sys.setrecursionlimit(10_000) # my my, now we're talking


def dfs(i, j, d, visited):
    if (i, j) == F:
        return d
    if (i, j) in visited:
        return 0
    visited.add((i, j))
    dirs = DIRS if grid[i][j] == "." else [CHEVRONS[grid[i][j]]]
    possible_nexts = [
        (i + di, j + dj)
        for di, dj in dirs
        if (0 <= i + dj < m and 0 <= j + dj < n and grid[i + di][j + dj] != "#")
    ]
    if not possible_nexts:
        return 0
    return max(dfs(ii, jj, d + 1, visited.copy()) for ii, jj in possible_nexts)


def compressed_dfs(i, j, d, visited):
    if (i, j) == F:
        return d
    if (i, j) in visited:
        return 0
    visited.add((i, j))
    return max(
        compressed_dfs(ii, jj, d + dd, visited.copy()) for dd, (ii, jj) in graph[(i, j)]
    )

def backtracked_dfs(i, j, d, visited:set):
    global longest
    if (i, j) == F:
        longest = max(longest, d)
    else:
        visited.add((i, j))
        for dd, (ii, jj) in graph[(i, j)]:
            if (ii, jj) not in visited:
                backtracked_dfs(ii, jj, d + dd, visited)
        visited.remove((i, j))



longest = 0
graph = defaultdict(set)


def compression():
    qq = deque()
    qq.append((S, []))
    vvisited = set()
    while qq:
        start, prev = qq.popleft()
        if start in vvisited:
            continue
        vvisited.add(start)
        q = deque()
        visited = [[False] * n for _ in range(m)]
        for ii, jj in prev:
            visited[ii][jj] = True
        q.append((start, 0))
        while q:
            (i, j), d = q.popleft()
            neigh = []
            for di, dj in DIRS:
                ii, jj = i + di, j + dj
                if 0 <= ii < m and 0 <= jj < n and grid[ii][jj] != "#":
                    neigh.append((ii, jj))
            if (len(neigh) > 2 or (i, j) == F) and (i, j) != start:
                graph[start].add((d, (i, j)))
                graph[(i, j)].add((d, start))
                qq.append(
                    (
                        (i, j),
                        [(ii, jj) for (ii, jj) in neigh if visited[ii][jj]]
                    )
                )
                continue

            for ii, jj in neigh:
                if not visited[ii][jj]:
                    visited[ii][jj] = True
                    q.append(((ii, jj), d + 1))


if __name__ == "__main__":
    with open("inputs/day23.txt") as f:
        whole_input = f.read()
    i0 = j0 = 0
    grid = whole_input.split("\n")
    m = len(grid)
    n = len(grid[0])

    j0 = 0
    j1 = 0
    while grid[0][j0] != ".":
        j0 += 1
    while grid[m - 1][j1] != ".":
        j1 += 1
    path = grid.copy()
    S = 0, j0
    F = m - 1, j1

    #print(f"    \u2022 first part: {dfs(*S, 0, set())}")
    mn, s = divmod(time() - start, 60)
    print(f"Done in {mn:.0f}m{s:.3f}s")
    start = time()

    compression()
    backtracked_dfs(*S, 0, set())
    print(f"    \u2022 second part: {longest}")
    mn, s = divmod(time() - start, 60)
    print(f"Done in {mn:.0f}m{s:.3f}s")