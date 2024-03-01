import re
from collections import defaultdict
from itertools import cycle
from math import sqrt
from time import time

if __name__ == "__main__":
    start = time()
    with open("inputs/day8.txt", "r") as f:
        lines = f.readlines()
    ptit_dic = {"L": 0, "R": 1}
    nodes = {}
    for line in lines[2:]:
        k, l, r = re.findall(r"[0-9A-Z]+", line)
        nodes[k] = (l, r)

    # ptr = 'AAA'
    # ans1 = 0
    # while ptr !="ZZZ":
    #     instrution = next(instrutions)
    #     ptr = nodes[ptr][ptit_dic[instrution]]
    #     ans1 += 1
    # print(ans1)

    def prime_factors(n):
        ans = defaultdict(int)
        while n % 2 == 0:
            ans[2] += 1
            n = n // 2
        for i in range(3, int(sqrt(n)) + 1, 2):
            while n % i == 0:
                ans[i] += 1
                n = n // i
        if n > 2:
            ans[n] += 1
        return ans

    def pppcm(numbers):
        ans_reducted = defaultdict(int)
        for n in numbers:
            primes = prime_factors(n)
            for p, exp in primes.items():
                ans_reducted[p] = max(exp, ans_reducted[p])
        ans = 1
        for p, exp in ans_reducted.items():
            ans *= p**exp
        return ans

    len_cycle_instruct = len(lines[0][:-1])
    ptrs = [k for k in nodes if k.endswith("A")]
    cycles = []
    instrutions = list(map(ptit_dic.get, lines[0][:-1]))
    for ptr in ptrs:
        steps = 0
        path = {}
        instrutions = cycle(instrutions)
        while (
            not ptr in path
            or path[ptr] % len_cycle_instruct != steps % len_cycle_instruct
        ):
            path[ptr] = steps
            instrution = next(instrutions)
            ptr = nodes[ptr][instrution]
            steps += 1

        cycles.append(steps - path[ptr])

    m, s = divmod(time() - start, 60)
    print(f"    \u2022 second part: {pppcm(cycles)}")
    print(f"Done in {m:.0f}m{s:.4f}s")
