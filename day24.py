import re
from time import time

import numpy as np

LOWER_BOUND = 200_000_000_000_000
UPPER_BOUND = 400_000_000_000_000


def get_coeffs(x0, v0x, y0, v0y, x1, v1x, y1, v1y):
    return (
        v0y - v1y,
        v1x - v0x,
        y0 - y1,
        x1 - x0,
        x1 * v1y - x0 * v0y + v0x * y0 - v1x * y1,
    )


def range_intersect(range1, range2):
    (x1inf, x1sup), (y1inf, y1sup) = range1
    (x2inf, x2sup), (y2inf, y2sup) = range2
    if x1inf > x2sup or y1inf > y2sup or x1sup < x2inf or y1sup < y2inf:
        return []
    return [
        (
            (max(x1inf, x2inf), min(x1sup, x2sup)),
            (
                max(y1inf, y2inf),
                min(y1sup, y2sup),
            ),
        )
    ]


if __name__ == "__main__":
    start = time()
    with open("inputs/day24.txt") as f:
        whole_input = f.read()
    rocks = []
    for line in whole_input.split("\n"):
        position, speed = line.split("@")
        rocks.append(
            (
                tuple(map(int, re.findall(r"[\-\d]+", position))),
                tuple(map(int, re.findall(r"[\-\d]+", speed))),
            )
        )
    ans = 0
    for i in range(len(rocks)):
        for j in range(i):
            (x1, y1, z1), (vx1, vy1, vz1) = rocks[i]
            (x2, y2, z2), (vx2, vy2, vz2) = rocks[j]
            det = vx2 * vy1 - vx1 * vy2
            if det == 0:
                continue
            t1 = (-vy2 * (x2 - x1) + vx2 * (y2 - y1)) * 1 / det
            t2 = (-vy1 * (x2 - x1) + vx1 * (y2 - y1)) * 1 / det
            if t1 < 0 or t2 < 0:
                continue
            x = vx1 * t1 + x1
            y = vy1 * t1 + y1
            if LOWER_BOUND <= x <= UPPER_BOUND and LOWER_BOUND <= y <= UPPER_BOUND:
                ans += 1

    print(f"    \u2022 first part: {ans}")

    # treeD_ranges = [[((-inf, inf), (-inf, inf))] for _ in range(3)]
    n = 0
    for i in range(len(rocks)):
        n += 1
        (x0, y0, z0), (v0x, v0y, v0z) = rocks[i]
        for j in range(i):
            n += 1
            (x1, y1, z1), (v1x, v1y, v1z) = rocks[j]
            for k in range(j):
                (x2, y2, z2), (v2x, v2y, v2z) = rocks[k]

                a11, a12, a14, a15, b1 = get_coeffs(x0, v0x, y0, v0y, x1, v1x, y1, v1y)
                a21, a23, a24, a26, b2 = get_coeffs(x0, v0x, z0, v0z, x1, v1x, z1, v1z)
                a32, a33, a35, a36, b3 = get_coeffs(y0, v0y, z0, v0z, y1, v1y, z1, v1z)
                a41, a42, a44, a45, b4 = get_coeffs(x2, v2x, y2, v2y, x1, v1x, y1, v1y)
                a51, a53, a54, a56, b5 = get_coeffs(x2, v2x, z2, v2z, x1, v1x, z1, v1z)
                a62, a63, a65, a66, b6 = get_coeffs(y2, v2y, z2, v2z, y1, v1y, z1, v1z)

                A = np.array(
                    [
                        [a11, a12, 0, a14, a15, 0],
                        [a21, 0, a23, a24, 0, a26],
                        [0, a32, a33, 0, a35, a36],
                        [a41, a42, 0, a44, a45, 0],
                        [a51, 0, a53, a54, 0, a56],
                        [0, a62, a63, 0, a65, a66],
                    ],
                    dtype=np.double,
                )
                B = np.array([b1, b2, b3, b4, b5, b6], dtype=np.double)
                n += 1
                if np.linalg.det(A) != 0:
                    break
            else:
                continue
            break
        else:
            continue
        break

    X = np.linalg.solve(A, B)

    print(f"    \u2022 second part: {(-X[0] - X[1] - X[2]).astype(int)}")
    mn, s = divmod(time() - start, 60)
    print(f"Done in {mn:.0f}m{s:.4f}s")

