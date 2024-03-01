import re
from collections import defaultdict
from time import time

start = time()

KEY_RE = re.compile(r"(.*){")
RULES_RE = re.compile(r"{(.*)}")
XMAS = {"x": 0, "m": 1, "a": 2, "s": 3, "": -1}


if __name__ == "__main__":
    start = time()
    with open("inputs/day19.txt", "r") as f:
        whole_input = f.read()
    wflows, pieces = whole_input.split("\n\n")
    wflow_dict = defaultdict(list)
    for wflow in wflows.split("\n"):
        key = KEY_RE.match(wflow).group(1)
        rules = RULES_RE.search(wflow).group(1).split(",")
        for rule in rules:
            try:
                cond, dest = rule.split(":")
                dim = cond[0]
                str_cond = cond[1:]
            except:
                dest, dim, str_cond = rule, "", ""
            wflow_dict[key].append((XMAS[dim], str_cond, dest))

    pieces = [
        tuple(map(int, re.findall(r"(?<=\=)[0-9]+", p))) for p in pieces.split("\n")
    ]
    state = {p: "in" for p in pieces}
    while not all(v == "A" or v == "R" for v in state.values()):
        for p in filter(lambda k: state[k] != "A" and state[k] != "R", state):
            for rule in wflow_dict[state[p]]:
                dim, str_cond, dest = rule
                if dim < 0:
                    state[p] = dest
                    break
                if str_cond[0] == "<" and p[dim] - int(str_cond[1:]) < 0:
                    state[p] = dest
                    break
                if str_cond[0] == ">" and p[dim] - int(str_cond[1:]) > 0:
                    state[p] = dest
                    break

    ans1 = sum(
        sum(dim for dim in piece) for piece in filter(lambda k: state[k] == "A", state)
    )
    print(f"    \u2022 first part: {ans1}")

    m, s = divmod(time() - start, 60)
    print(f"Done in {m:.0f}m{s:.4f}s")
    start = time()
    #### part 2 #####
    ans2 = 0
    state2 = {tuple((1, 4000) for _ in range(4)): "in"}
    while not all(v == "A" or v == "R" for v in state2.values()):
        state2_next = {}
        for t_rang_ in filter(lambda k: state2[k] == "A", state2):
            (a, b), (c, d), (e, f), (g, h) = t_rang_
            ans2 += (1 + b - a) * (1 + d - c) * (1 + f - e) * (1 + h - g)
        for t_rang_ in filter(lambda k: state2[k] != "A" and state2[k] != "R", state2):
            for rule in wflow_dict[state2[t_rang_]]:
                dim, str_cond, dest = rule
                if dim < 0:
                    state2_next[t_rang_] = dest
                    break
                if str_cond[0] == "<":
                    if t_rang_[dim][1] < int(str_cond[1:]):
                        state2_next[t_rang_] = dest
                        break
                    if t_rang_[dim][0] >= int(str_cond[1:]):
                        continue
                    t_rang_1 = list(list(ran_) for ran_ in t_rang_)
                    t_rang_1[dim] = [t_rang_1[dim][0], int(str_cond[1:]) - 1]
                    t_rang_2 = list(list(ran_) for ran_ in t_rang_)
                    t_rang_2[dim] = [int(str_cond[1:]), t_rang_2[dim][1]]
                    state2_next[tuple(tuple(ran_) for ran_ in t_rang_1)] = dest
                    t_rang_ = tuple(tuple(ran_) for ran_ in t_rang_2)

                if str_cond[0] == ">":
                    if t_rang_[dim][0] > int(str_cond[1:]):
                        state2_next[t_rang_] = dest
                        break
                    if t_rang_[dim][1] <= int(str_cond[1:]):
                        continue
                    t_rang_1 = list(list(ran_) for ran_ in t_rang_)
                    t_rang_1[dim] = [t_rang_1[dim][0], int(str_cond[1:])]
                    t_rang_2 = list(list(ran_) for ran_ in t_rang_)
                    t_rang_2[dim] = [int(str_cond[1:]) + 1, t_rang_2[dim][1]]
                    state2_next[tuple(tuple(ran_) for ran_ in t_rang_2)] = dest
                    t_rang_ = tuple(tuple(ran_) for ran_ in t_rang_1)

        state2 = state2_next

    for t_rang_ in filter(lambda k: state2[k] == "A", state2):
        (a, b), (c, d), (e, f), (g, h) = t_rang_
        ans2 += (1 + b - a) * (1 + d - c) * (1 + f - e) * (1 + h - g)
    print(f"    \u2022 second part: {ans2}")
    m, s = divmod(time() - start, 60)
    print(f"Done in {m:.0f}m{s:.4f}s")
