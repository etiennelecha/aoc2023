import re

# true ans1 54967
# true ans2 54885
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
    ans3 = 0
    pattern = r"[0-9]|eightwo|twone|sevenine|fiveight|oneight|nineight|threeight|one|two|three|four|five|six|seven|eight|nine"
    pattern2 = r"(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))"
    numbers = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "sevenine": "79",
        "oneight": "18",
        "eight": "8",
        "fiveight": "58",
        "threight": "38",
        "nineight": "98",
        "nine": "9",
        "eightwo": "82",
        "twone": "21",
    }
    for line in lines:
        digits = re.findall(pattern, line)
        digits2 = re.findall(pattern2, line)
        digit = (
            numbers.get(digits[0], digits[0])[0]
            + numbers.get(digits[-1], digits[-1])[-1]
        )
        digit2 = numbers.get(digits2[0], digits2[0]) + numbers.get(
            digits2[-1], digits2[-1]
        )
        print(f"digit2 {digit2}")
        ans2 += int(digit)
        ans3 += int(digit2)
    print(f"    \u2022 second part: {ans2}")
    # print(f"    \u2022 ref second part: {ans3}")
