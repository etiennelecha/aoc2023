import re
from functools import lru_cache
from time import time

if __name__ == "__main__":
    start = time()
    with open("inputs/day4.txt", "r") as f:
        lines = f.readlines()
    ans1 = 0
    counts_matches = {}

    for i, line in enumerate(lines):
        winning_string = line[line.find(":") : line.find("|")]
        draw_string = line[line.find("|") :]
        set_wins = set(re.findall(r"[0-9]+", winning_string))
        count_wins = len(
            list(filter(lambda s: s in set_wins, re.findall(r"[0-9]+", draw_string)))
        )
        counts_matches[i + 1] = count_wins
        if count_wins >= 1:
            ans1 += 2 ** (count_wins - 1)

    @lru_cache(None)
    def process(card):
        return 1 + sum([process(card + j) for j in range(1, counts_matches[card] + 1)])

    ans2 = sum(process(j) for j in range(1, len(lines) + 1))
    m, s = divmod(time() - start, 60)

    print(f"    \u2022 first part: {ans1}")
    print(f"    \u2022 second part: {ans2}")
    print(f"Done in {m:.0f}m{s:.3f}s")
