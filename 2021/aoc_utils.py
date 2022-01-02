import copy
import io
import heapq
import numpy as np
from collections import deque

HEX2BIN = {
    '0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111',
    '8': '1000', '9': '1001', 'a': '1010', 'b': '1011', 'c': '1100', 'd': '1101', 'e': '1110', 'f': '1111'
}

def read_lines(f):
    with open(f, 'r') as fp:
        return fp.readlines()


def read_lines_int(f):
    with open(f, 'r') as fp:
        ln = fp.readlines()
        return [int(x) for x in ln]


def read_lines_int_matrix(f):
    with open(f, 'r') as fp:
        ln = fp.readlines()
        return [[int(c) for c in l.strip()] for l in ln]


def read_lines_lazy(f):
    with open(f, 'r') as fp:
        while True:
            ln = fp.readline()
            if ln:
                yield ln
            else:
                break


def read_lines_int_lazy(f):
    for ln in read_lines_lazy(f):
        yield int(ln)


def sliding_window(en, size):
    window = deque([], maxlen=size)
    cnt = 0
    for i in en:
        if cnt == size:
            window.popleft()
        else:
            cnt += 1
        window.append(i)
        yield list(window)
    while cnt > 1:
        window.popleft()
        cnt -= 1
        yield list(window)


def bin_to_num(bstr: str):
    g = 0
    bstr = bstr.strip()
    for i in range(len(bstr)):
        g <<= 1
        if bstr[i] == '1':
            g |= 1
    return g


def sign(x):
    return 0 if x == 0 else (-1 if x < 0 else 1)


def arithmetic(a1, d, n):
    return (n * (a1 + a1 + (n - 1) * d)) / 2


def get_neighbors(m, x, y):
    return {
        'l': m[y][x - 1] if x > 0 else None,
        't': m[y - 1][x] if y > 0 else None,
        'r': m[y][x + 1] if x < (len(m[y]) - 1) else None,
        'b': m[y + 1][x] if y < (len(m) - 1) else None
    }


def get_neighbors_coord(m, x, y, diag=False, self=False):
    nb = []

    if diag and x > 0 and y > 0:
        nb.append((x - 1, y - 1))
    if y > 0:
        nb.append((x, y - 1))
    if diag and x < (len(m[y]) - 1) and y > 0:
        nb.append((x + 1, y - 1))

    if x > 0:
        nb.append((x - 1, y))
    if self:
        nb.append((x, y))
    if x < (len(m[y]) - 1):
        nb.append((x + 1, y))

    if diag and x > 0 and y < (len(m) - 1):
        nb.append((x - 1, y + 1))
    if y < (len(m) - 1):
        nb.append((x, y + 1))
    if diag and x < (len(m[y]) - 1) and y < (len(m) - 1):
        nb.append((x + 1, y + 1))

    return nb


def iter2d(w, h, l=0, t=0):
    for y in range(t, t+h):
        for x in range(l, l + w):
            yield x, y


def find_all_paths(graph, start='start', end='end', revisit_rule=lambda n, p: False):
    if start not in graph or end not in graph or len(graph[start]) == 0 or len(graph[end]) == 0:
        return []

    paths = deque()
    stack = deque()

    stack.appendleft([start])
    while stack:
        path = stack.popleft()
        last = path[-1]
        if last == end:
            paths.append(path)
            continue

        neighbors = graph[last]
        for n in neighbors:
            if n not in path or revisit_rule(n, path):
                stack.appendleft(path + [n])

    return list(paths)


def count_elements(l):
    d = {}
    for i in l:
        d[i] = d.get(i, 0) + 1
    return d


def dict_least_most_items(d: dict):
    u = max(d.values())
    l = min(d.values())
    U = L = None
    for k, v in d.items():
        if u == v:
            U = k
        if l == v:
            L = k
    return L, U


def merge_counts(a: dict, b: dict):
    n = copy.copy(a)
    for k, v in b.items():
        if k in n:
            n[k] += v
        else:
            n[k] = v
    return n


def dijkstra(E:dict, V:list, s, t=None):
    # Initialize distances and backtracking info
    p = dict.fromkeys(V, None)
    d = dict([(v, [float('inf'), v]) for v in V])
    d[s][0] = 0

    # Initialize priority queue
    Q = [lst for lst in d.values()]
    heapq.heapify(Q)

    # Repeat until done
    while Q:
        _, u = heapq.heappop(Q)

        # Break when target has been reached
        if t is not None and u == t:
            break

        # Update neighbors
        for neighbor, dst in E[u]:
            alt = d[u][0] + dst
            if alt < d[neighbor][0]:
                d[neighbor][0] = alt
                p[neighbor] = u
                heapq.heapify(Q)

    # Return dictionary of distances when target is not specified
    if t is None:
        return dict([(k, v[0]) for k, v in d.items()])

    # Reconstruct path
    P = deque()
    u = t
    while p[u] is not None:
        P.appendleft(u)
        u = p[u]

    return list(P), d[t][0]


def bfs_evaluate_paths(grid, s, diag=False):
    dists = np.full((len(grid), len(grid[-1])), -1)
    visited = np.full(dists.shape, False)
    dists[s[1]][s[0]] = 0
    visited[s[1]][s[0]] = True
    q = deque([s])
    while q:
        pt = q.popleft()
        for n in get_neighbors_coord(grid, pt[0], pt[1], diag):
            d = dists[pt[1]][pt[0]] + grid[n[1]][n[0]]
            v = visited[n[1]][n[0]]
            if not v or d < dists[n[1]][n[0]]:
                dists[n[1]][n[0]] = d
                q.append(n)
                visited[n[1]][n[0]] = True
    return dists


def hex2bin(msg):
    global HEX2BIN
    return ''.join(map(lambda x: HEX2BIN[x], msg.lower()))


def is_number(x):
    return isinstance(x, (int, float))