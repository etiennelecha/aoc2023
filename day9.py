import re
from functools import reduce
from itertools import pairwise
from time import time

if __name__ == "__main__":
    start = time()
    with open("inputs/day9.txt", "r") as f:
        lines = f.readlines()

    ans1 = 0
    ans2 = 0
    for line in lines:
        nums = list(map(int, re.findall(r"-*[0-9]+", line)))
        lasts = []
        firsts = []
        while not all(num == 0 for num in nums):
            lasts.append(nums[-1])
            firsts.append(nums[0])
            nums = list(map(lambda t: t[1] - t[0], pairwise(nums)))
        ans1 += sum(lasts)
        firsts.append(0)
        ans2 += reduce(lambda x, y: y - x, firsts[::-1])
        
    print(ans1)
    print(ans2)
