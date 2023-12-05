import re
from time import time

if __name__ == "__main__":
    start = time()
    with open("inputs/day5.txt", "r") as f:
        lines = f.readlines()
    seeds = list(map(int, re.findall(r"[0-9]+", lines[0])))
    seeds_but_ranges = []
    iter_seeds = iter(seeds)
    this_seed = next(iter_seeds, None)
    while this_seed:
        seeds_but_ranges.append((this_seed, this_seed + next(iter_seeds) - 1))
        this_seed = next(iter_seeds, None)

    blocks = [[], [], [], [], [], [], []]
    iter_lines = iter(lines[1:])
    iter_blocks = iter(blocks)
    this_line = next(iter_lines, None)
    while this_line:
        while this_line and not re.search(r"[0-9]", this_line):
            this_line = next(iter_lines, None)
        this_block = next(iter_blocks)
        while this_line and re.search(r"[0-9]", this_line):
            this_block.append(tuple(map(int, re.findall(r"[0-9]+", this_line))))
            this_line = next(iter_lines, None)

    def travel(traveler):
        iter_blocks = iter(blocks)
        block = next(iter_blocks, None)
        while block:
            for dst, src, length in block:
                if src <= traveler <= src + length - 1:
                    traveler += dst - src
                    break
            block = next(iter_blocks, None)
        return traveler

    def sections(range1, base_range):
        l1, r1 = range1
        lb, rb = base_range
        if r1 < lb or l1 > rb:
            return [range1], ()
        if l1 < lb:
            if r1 > rb:
                return [(l1, lb - 1), (rb + 1, r1)], (lb, rb)
            else:
                return [(l1, lb - 1)], (lb, r1)
        if r1 > rb:
            return [(rb + 1, r1)], (l1, rb)
        else:
            return [], (l1, r1)

    def union(range, sorted_ranges):
        # sorted_ranges DISJOINT AND SORTED
        l, r = range
        len_ = len(sorted_ranges)
        if len_ == 0:
            return [range]
        insert_l = -1
        insert_r = -1
        for i, (lo, ro) in enumerate(sorted_ranges[::-1]):
            if ro < l - 1:
                if i == 0:
                    return sorted_ranges + [range]
                insert_l = len_ - i - 1  # untouched UPTO THIS INDEX
                new_l = min(l, sorted_ranges[insert_l + 1][0])
                break
        if insert_l < 0:
            new_l = min(l, sorted_ranges[0][0])
        for j, (lo, ro) in enumerate(sorted_ranges):
            if lo > r + 1:
                if j == 0:
                    return [range] + sorted_ranges
                insert_r = j
                new_r = max(r, sorted_ranges[insert_r - 1][1])
                break
        if insert_r < 0:
            new_r = max(r, sorted_ranges[-1][1])
            insert_r = len_
        return (
            sorted_ranges[: insert_l + 1] + [(new_l, new_r)] + sorted_ranges[insert_r:]
        )

    def travel_range(ranges):
        iter_blocks = iter(blocks)
        block = next(iter_blocks, None)
        while block:
            hit_ranges = []
            for dst, src, length in block:
                split_ranges = []
                for ran in ranges:
                    misses, hit_range = sections(ran, (src, src + length - 1))
                    split_ranges += misses
                    if hit_range:
                        l, r = hit_range
                        hit_ranges.append((l + dst - src, r + dst - src))
                ranges = split_ranges
            for ran in hit_ranges:
                ranges = union(ran, ranges)
            block = next(iter_blocks, None)
        return ranges[0][0]

    sorted_seeds = []
    for range_ in seeds_but_ranges:
        sorted_seeds = union(range_, sorted_seeds)

    travelers = map(travel, seeds)
    ans2 = travel_range(sorted_seeds)
    m, s = divmod(time() - start, 60)

    print(f"    \u2022 first part: {min(map(travel, seeds))}")
    print(f"    \u2022 second part: {ans2}")
    print(f"Done in {m:.0f}m{s:.4f}s")
