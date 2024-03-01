import re
from functools import lru_cache
from time import time

W_REGEX = re.compile(r"\.+")

with open("inputs/day12.txt") as f:
    lines = f.read()
start = time()

@lru_cache
def get_regex(i):
    """
    Returns a pattern which matches a group of one or more machines which has exactly the given length.
    Uses an LRU cache so that we don't recompile the same patterns again and again
    """
    return re.compile(r"[\#\?]{%i}(\.|\?|$)" % i)

@lru_cache
def arrangement_counter(springs: str, pattern: tuple) -> int:
    if not springs:
        if pattern:
            return 0
        return 1
    if not pattern:
        if "#" in springs:
            return 0
        return 1
    
    removable_m = W_REGEX.match(springs)
    if removable_m:
        return arrangement_counter(springs[len(removable_m.group()) :], pattern)
    ans = 0
    # string start with ? or #
    if springs[0] == "?":
        ans += arrangement_counter(springs[1:], pattern)

    curr_block = pattern[0]
    possible_fit_m = get_regex(curr_block).match(springs)
    if possible_fit_m:
        remaining_blocks = pattern[1:]
        # Assume all machines in this range are broken.
        ans += arrangement_counter(
            springs[len(possible_fit_m.group()) :], remaining_blocks
        )

    return ans


ans1 = 0

for line in lines.split("\n"):
    springs, pattern = line.split(" ")
    damaged = tuple([int(e) for e in pattern.split(",")])
    arrangements = arrangement_counter(springs, damaged)
    ans1 += arrangements

ans2 = 0

for i, line in enumerate(lines.split("\n")):
    springs, pattern = line.split(" ")
    springs = "?".join([springs for _ in range(5)])
    pattern = ",".join([pattern for _ in range(5)])
    damaged = tuple([int(d) for d in pattern.split(",")])
    arrangements = arrangement_counter(springs, damaged)
    ans2 += arrangements

m, s = divmod(time() - start, 60)

print(f"    \u2022 first part: {ans1}")
print(f"    \u2022 second part: {ans2}")
print(f"Done in {m:.0f}m{s:.4f}s")