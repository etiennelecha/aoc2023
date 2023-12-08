from collections import Counter
from time import time

start = time()

class Hand:
    CONV = {
        "A": "a",
        "K": "b",
        "Q": "c",
        "J": "d",
        "T": "e",
        "9": "f",
        "8": "g",
        "7": "h",
        "6": "i",
        "5": "j",
        "4": "k",
        "3": "l",
        "2": "m",
    }
    CONV2 = CONV.copy()
    CONV2.update({"J": "n"})

    def __init__(self, line: str, conv_dict) -> None:
        hand, bid = line.split(" ")
        self.hand = "".join(conv_dict[c] for c in hand)
        self.bid = int(bid)
        dict_ = Counter(self.hand)
        jays = dict_.get("n", 0)
        if 0 < jays < 5:
            dict_ = {k: v for (k, v) in dict_.items() if k != "n"}
            c = max(dict_, key=lambda k: dict_[k])
            dict_[c] += jays
        if len(dict_) == 1:
            self.type = 1
        elif max(dict_.values()) == 4:
            self.type = 2
        elif max(dict_.values()) == 3:
            if len(dict_) == 2:
                self.type = 3
            else:
                self.type = 4
        elif max(dict_.values()) == 2:
            if len(dict_) == 3:
                self.type = 5
            else:
                self.type = 6
        else:
            self.type = 7

    def __lt__(self, other):
        if self.type == other.type:
            return self.hand > other.hand
        return self.type > other.type



if __name__ == "__main__":
    with open("inputs/day7.txt", "r") as f:
        lines = f.readlines()
        hands1 = [Hand(line, conv_dict=Hand.CONV) for line in lines]
        hands2 = [Hand(line, conv_dict=Hand.CONV2) for line in lines]
    hands1.sort()
    hands2.sort()
    ans1 = 0
    ans2 = 0
    for i, hand in enumerate(hands1):
        ans1 += (i + 1) * hand.bid
    for i, hand in enumerate(hands2):
        ans2 += (i + 1) * hand.bid
    
    m, s = divmod(time() - start, 60)
    print(f"    \u2022 first part: {ans1}")
    print(f"    \u2022 second part: {ans2}")
    print(f"Done in {m:.0f}m{s:.4f}s")
