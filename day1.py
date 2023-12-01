import re

if __name__ == "__main__":
    with open("inputs/day1.txt", "r") as f:
        lines = f.readlines()
    ans1 = 0
    for line in lines:
        digits = re.findall(r"[0-9]", line)
        digit = digits[0] + digits[-1]
        ans1 += int(digit)
    print(f"    \u2022 first part: {ans1}")
    ans2 = 0
    pattern = r"(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))"
    numbers = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    for line in lines:
        digits = re.findall(pattern, line)
        digit = numbers.get(digits[0], digits[0]) + numbers.get(digits[-1], digits[-1])
        ans2 += int(digit)
    print(f"    \u2022 second part: {ans2}")
    