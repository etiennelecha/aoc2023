from time import time


if __name__ == "__main__":
    start = time()

    with open("inputs/day11.txt", "r") as f:
        lines = f.read()
    grid = lines.split("\n")
    m = len(grid)
    n = len(grid[0])
    empty_rows = []
    empty_cols = []
    for i in range(m):
        if grid[i] == "." * n:
            empty_rows.append(i)
    for j in range(n):
        if all(grid[i][j] == "." for i in range(m)):
            empty_cols.append(j)
    galaxies = []
    ans1 = 0
    ans2 = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "#":
                for io, jo in galaxies:
                    d_row = len([r for r in empty_rows if i < r < io or io < r < i])
                    d_col = len([c for c in empty_cols if j < c < jo or jo < c < j])
                    num1 = d_col + abs(i - io) + d_row + abs(j - jo)
                    num2 = 999_998 * (d_col + d_row) + num1
                    ans1 += num1
                    ans2 += num2
                galaxies.append((i, j))

    m, s = divmod(time() - start, 60)

    print(f"    \u2022 first part: {ans1}")
    print(f"    \u2022 second part: {ans2}")
    print(f"Done in {m:.0f}m{s:.4f}s")
