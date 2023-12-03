import re

if __name__ == "__main__":
    with open("inputs/day3.txt", "r") as f:
        big_table = list(map(list, f.readlines()))
        big_table[-1] += "\n"
    ans1 = 0
    symbols = "*$+-%#&=/@"
    numbers = "0123456789"
    m = len(big_table)
    n = len(big_table[0]) - 1
    big_table = (
        [["."] * (n + 2)]
        + [["."] + line[:-1] + ["."] for line in big_table]
        + [["."] * (n + 2)]
    )

    def get_number(i, j) -> int:
        if big_table[i][j] not in numbers:
            return 0
        ans = ""
        k = j
        l = j + 1
        while big_table[i][k] in numbers:
            ans = big_table[i][k] + ans
            big_table[i][k] = "."
            k -= 1
        while big_table[i][l] in numbers:
            ans = ans + big_table[i][l]
            big_table[i][l] = "."
            l += 1
        return int(ans)

    i = 1
    while i < m + 1:
        j = 1
        while j < n + 1:
            if big_table[i][j] in symbols:
                ans1 += get_number(i, j - 1)
                ans1 += get_number(i, j + 1)
                ans1 += get_number(i + 1, j - 1)
                ans1 += get_number(i + 1, j)
                ans1 += get_number(i + 1, j + 1)
                ans1 += get_number(i - 1, j - 1)
                ans1 += get_number(i - 1, j)
                ans1 += get_number(i - 1, j + 1)
            j += 1
        i += 1
    print(f"    \u2022 first part: {ans1}")

    with open("inputs/day3.txt", "r") as f:
        big_table = list(map(list, f.readlines()))
        big_table[-1] += "\n"
    ans2 = 0
    big_table = (
        [["."] * (n + 2)]
        + [["."] + line[:-1] + ["."] for line in big_table]
        + [["."] * (n + 2)]
    )

    def get_number_2(i, j):
        numstring = ""
        positions = set()
        k = j
        l = j + 1
        while big_table[i][k] in numbers:
            numstring = big_table[i][k] + numstring
            positions.add((i, k))
            k -= 1
        while big_table[i][l] in numbers:
            numstring = numstring + big_table[i][l]
            l += 1
            positions.add((i, l))
        return int(numstring), positions

    i = 1
    while i < m + 1:
        j = 1
        while j < n + 1:
            if big_table[i][j] == "*":
                l = (big_table[i][j - 1], (i, j - 1))
                tl = (big_table[i - 1][j - 1], (i - 1, j - 1))
                t = (big_table[i - 1][j], (i - 1, j))
                tr = (big_table[i - 1][j + 1], (i - 1, j + 1))
                r = (big_table[i][j + 1], (i, j + 1))
                br = (big_table[i + 1][j + 1], (i + 1, j + 1))
                b = (big_table[i + 1][j], (i + 1, j))
                bl = (big_table[i + 1][j - 1], (i + 1, j - 1))
                count = len(
                    re.findall(
                        r"[0-9]+",
                        l[0] + tl[0] + t[0] + tr[0] + r[0] + br[0] + b[0] + bl[0],
                    )
                )
                if count == 2:
                    ratio = 1
                    positions = set()
                    for pix, (k, l) in [l, tl, t, tr, r, br, b, bl]:
                        if pix in numbers:
                            f, set_pos = get_number_2(k, l)
                            if len(set_pos & positions) == 0:
                                ratio *= f
                                positions |= set_pos
                    ans2 += ratio
            j += 1
        i += 1
    print(f"    \u2022 second part: {ans2}")
