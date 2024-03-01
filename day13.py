from time import time

with open("inputs/day13.txt") as f:
    whole_input = f.read()
start = time()
blocks = whole_input.split("\n\n")

def is_reflection(start_idx, lines):
    di = 0
    l = len(lines)
    while lines[start_idx - di] == lines[start_idx + 1 + di]:
        if (start_idx - di) == 0 or (start_idx + 1 + di) == l - 1:
            return start_idx + 1
        di += 1
    return 0

def diff_count(line1, line2):
    return len(list(filter(lambda t: t[0] != t[1],  zip(line1, line2))))

def is_pseudo_reflection(start_idx, lines):
    smidge = 1
    di = 0
    l = len(lines)
    diff = diff_count(lines[start_idx - di], lines[start_idx + 1 + di])
    while diff <= smidge:
        smidge -= diff
        if (start_idx - di) == 0 or (start_idx + 1 + di) == l - 1:
            return start_idx + 1 if smidge == 0 else 0
        di += 1
        diff = diff_count(lines[start_idx - di], lines[start_idx + 1 + di])
    return 0

if __name__ == "__main__":
    ans1 = 0
    ans2 = 0
    for block in blocks:
        h_lines = block.split("\n")
        m = len(h_lines)
        v_lines = ["".join(line[i] for line in h_lines) for i in range(len(h_lines[0]))]
        n = len(v_lines)
        i = 0
        j = 0
        while i < m - 1:
            ans2 += 100 * is_pseudo_reflection(i, h_lines)
            if h_lines[i] == h_lines[i + 1]:
                ans1 += 100 * is_reflection(i, h_lines)
            i += 1
        
        while j < n - 1:
            ans2 += is_pseudo_reflection(j, v_lines)
            if v_lines[j] == v_lines[j + 1]:
                ans1 += is_reflection(j, v_lines)
            j += 1

    m, s = divmod(time() - start, 60)
    print(f"    \u2022 first part: {ans1}")
    print(f"    \u2022 second part: {ans2}")
    print(f"Done in {m:.0f}m{s:.4f}s")
                