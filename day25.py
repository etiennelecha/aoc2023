import re
from heapq import heapify, heappop, heappush
from math import inf
from time import time

import matplotlib.pyplot as plt
import networkx as nx


def min_(pair1, pair2):
    int1, v1 = pair1
    int2, v2 = pair2
    if int1 < int2:
        return pair1
    if int2 < int1:
        return pair2
    for i, j in zip(v1, v2):
        if i < j:
            return pair1
        if j < i:
            return pair2
    return pair1


def global_min_cut(adj_matrix):
    best = inf, []
    n = len(adj_matrix)
    co = []

    for i in range(n):
        co.append([i])

    for _ in range(1, n):
        w = adj_matrix[0]
        s, t = 0, 0
        h = heapify([0, s, t])
        while h:
            _, s, t = heappop(h)
            w[t] = -inf
            s = t
            t = max(range(n), key=lambda i: w[i])
            for i in range(n):
                w[i] += adj_matrix[t][i]
            heappush(h, (w[s], s, t))
        best = min_(best, (w[t] - adj_matrix[t][t], co[t]))
        co[s] += co[t]
        for i in range(n):
            adj_matrix[s][i] += adj_matrix[t][i]
        for i in range(n):
            adj_matrix[i][s] += adj_matrix[s][i]
        adj_matrix[0][t] = inf
    return best


if __name__ == "__main__":
    start = time()
    with open("inputs/day25.txt") as f:
        whole_input = f.read()
    adj_list = {}
    for line in whole_input.split('\n'):
        nodes = re.findall(r'[a-z]+', line)
        adj_list[nodes[0]] = nodes[1:]
    G = nx.Graph(adj_list)
    #nx.draw(G)
    #plt.show()

    cut_value, partition = nx.stoer_wagner(G)
    print(f"    \u2022 first part: {len(partition[0]) * len(partition[1])}")
    m, s = divmod(time() - start, 60)
    print(f"Done in {m:.0f}m{s:.4f}s")