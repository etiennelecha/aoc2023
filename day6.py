import re
from functools import reduce
from math import floor, sqrt
from time import time

if __name__ == "__main__":
    start = time()
    with open("inputs/day6.txt", "r") as f:
        lines = f.readlines()
    times = list(map(int, re.findall(r"[0-9]+", lines[0])))
    distances = list(map(int, re.findall(r"[0-9]+", lines[1])))
    ans1 = 1
    for total_time, distance in zip(times, distances):
        count_beat = 0
        for t in range(1, total_time):
            if t * (total_time - t) > distance:
                count_beat += 1
        ans1 *= count_beat

    big_time = int(reduce(lambda a, b: a + b, re.findall(r"[0-9]+", lines[0])))
    big_dist = int(reduce(lambda a, b: a + b, re.findall(r"[0-9]+", lines[1])))
    ans2 = floor(sqrt(big_time ** 2 - 4 * big_dist))

    m, s = divmod(time() - start, 60)

    print(f"    \u2022 first part: {ans1}")
    print(f"    \u2022 second part: {ans2}")
    print(f"Done in {m:.0f}m{s:.4f}s")

