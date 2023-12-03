import re

if __name__ == "__main__":
    with open("inputs/day2.txt", "r") as f:
        lines = f.readlines()
    ans1 = 0
    ans2 = 0
    for i, line in enumerate(lines):
        blues = re.findall(r"[0-9]+(?= blue)", line)
        reds = re.findall(r"[0-9]+(?= red)", line)
        greens = re.findall(r"[0-9]+(?= green)", line)

        is_ok_red = all(int(x) <= 12 for x in reds)
        is_ok_green = all(int(x) <= 13 for x in greens)
        is_ok_blue = all(int(x) <= 14 for x in blues)
        if is_ok_blue and is_ok_green and is_ok_red:
            ans1 += i + 1

        ans2 += max(map(int, reds)) * max(map(int, blues)) * max(map(int, greens))

    print(f"    \u2022 first part: {ans1}")
    print(f"    \u2022 second part: {ans2}")
