from collections import defaultdict, deque
from math import lcm
from time import time


def process(q, state, nsteps):
    n_high = 0
    n_low = 0
    while q:
        module_from, pulse, module = q.popleft()
        if module in config:
            if config[module][0] == "broadcaster":
                for succ in config[module][1]:
                    q.append(("broadcaster", pulse, succ))
                    n_low += 1
            elif config[module][0] == "%" and not pulse:
                state[module] = not (state[module])
                for succ in config[module][1]:
                    q.append((module, state[module], succ))
                    if state[module]:
                        n_high += 1
                    else:
                        n_low += 1
            elif config[module][0] == "&":
                state[module][module_from] = pulse
                inputs_all = all(v for v in state[module].values())
                for succ in config[module][1]:
                    q.append((module, not (inputs_all), succ))
                    if inputs_all:
                        n_low += 1
                    else:
                        n_high += 1

    return n_high, n_low, state


def button(state, start, nsteps):
    q = deque()
    q.append(("button", False, start))
    n_high, n_low, state = process(q, state, nsteps)
    return state, n_high, n_low + 1


def cycle(state_start, start):
    n_high, n_low = 0, 0
    n_steps = 0
    state = state_start
    r_state = str(state)
    while r_state not in states_reached:
        states_reached[r_state] = n_steps
        state, ih, il = button(state, start, n_steps)
        n_steps += 1
        r_state = str(state)
        n_high += ih
        n_low += il
    return n_high, n_low, n_steps - states_reached[r_state]


if __name__ == "__main__":
    t_start = time()
    with open("inputs/day20.txt", "r") as f:
        lines = f.readlines()

    config = {}
    state_zero = {}
    preds = defaultdict(list)
    rails = []
    for line in lines:
        module, connected_modules = line.split(" -> ")
        successors = list(map(lambda s: s.strip(), connected_modules.split(",")))
        name = module[1:] if not module[0].isalpha() else module
        type_ = module[0] if not module[0].isalpha() else module
        config[name] = (type_, tuple(successors))

    for module, (type_, succs) in config.items():
        for succ in succs:
            if succ in config:
                preds[succ].append(module)
    for module, (type_, _) in config.items():
        if type_ == "%":
            state_zero[module] = False
        elif type_ == "&":
            state_zero[module] = {mod: False for mod in preds[module]}
    succ_dict = {
        k: successors
        for k, (_, successors) in config.items()
        if k != "broadcaster" and k != "bq"
    }
    broadcaster_dict = {
        k: successors for k, (_, successors) in config.items() if k == "broadcaster"
    }

    starts = broadcaster_dict["broadcaster"]
    cycles = []

    for start in starts:
        states_reached = {}
        n_high, n_low, n_steps = cycle(state_zero, start)
        cycles.append(n_steps)

    print(f"    \u2022 second part: {lcm(*cycles)}")
    m, s = divmod(time() - t_start, 60)
    print(f"Done in {m:.0f}m{s:.4f}s")
