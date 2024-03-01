from collections import defaultdict, deque
from itertools import product
from time import time

start = time() 
class Point:
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z


class Brick:
    def __init__(self, p1, p2, id) -> None:
        if p1.z < p2.z:
            self.start = p1
            self.end = p2
        else:
            self.start = p2
            self.end = p1
        self.id = id
        self.widthx = 1 + abs(self.end.x - self.start.x)
        self.widthy = 1 + abs(self.end.y - self.start.y)
        self.x0 = min(self.start.x, self.end.x)
        self.y0 = min(self.start.y, self.end.y)
        self.is_supported_by = set()

    def fall_to(self, z0):
        self.end.z += z0 - self.start.z
        self.start.z = z0


if __name__ == "__main__":
    with open("inputs/day22.txt") as f:
        whole_input = f.read()

    lines = whole_input.split("\n")
    bricks = []
    for i, line in enumerate(lines):
        p1, p2 = line.split("~")
        p1 = Point(*(list(map(int, p1.split(",")))))
        p2 = Point(*(list(map(int, p2.split(",")))))
        bricks.append(Brick(p1, p2, i))

    bricks.sort(key=lambda b: b.start.z)
    elevations_map = defaultdict(lambda : (0, None))
    final_state = []

    for b in bricks:
        curr_height = max(
            elevations_map[(x,y)][0]
            for x, y in product(
                range(b.x0, b.x0 + b.widthx), range(b.y0, b.y0 + b.widthy)
            )
        )
        
        b.fall_to(curr_height + 1)
        
        for x, y in product(range(b.x0, b.x0 + b.widthx), range(b.y0, b.y0 + b.widthy)):
            prev_height, sup = elevations_map[x,y]
            if prev_height == curr_height and sup is not None:
                b.is_supported_by.add(sup)
            elevations_map[x,y] = (b.end.z, b.id)
        final_state.append(b)

    crucial_b = set()
    is_supported_by = [[] for _ in range(len(final_state))]
    supports = [[] for _ in range(len(final_state))]
    for b in final_state:
        is_supported_by[b.id] += list(b.is_supported_by)
        for poutre in b.is_supported_by:
            supports[poutre].append(b.id)
    ans1 = 0
    ans2 = 0
    
    for bid in range(len(final_state)):
        fallen = [False] * len(final_state)
        fallen[bid] = True
        q = deque()
        q.append(bid)
        useless = True
        while q:
            curr = q.popleft()
            for up_poutre in supports[curr]:
                if (
                    all(fallen[i] for i in is_supported_by[up_poutre])
                    and not fallen[up_poutre]
                ):
                    ans2 += 1
                    fallen[up_poutre] = True
                    q.append(up_poutre)
                    useless = False
        if useless:
            ans1 += 1

    print(f"    \u2022 first part: {ans1}")
    print(f"    \u2022 second part: {ans2}")
    m, s = divmod(time() - start, 60)
    print(f"Done in {m:.0f}m{s:.4f}s")
