from itertools import product
from collections import deque
from math import sqrt
from aoc_utils import read_lines_lazy


# SOME SETTINGS
CUBE_SIZE = 1000
MATCH_NUM_REQUIRED = 12
VALID_ORIENTATIONS = [
    lambda x, y, z: (+x, +y, +z),
    lambda x, y, z: (+x, +z, -y),
    lambda x, y, z: (+x, -y, -z),
    lambda x, y, z: (+x, -z, +y),
    lambda x, y, z: (+y, +x, -z),
    lambda x, y, z: (+y, +z, +x),
    lambda x, y, z: (+y, -x, +z),
    lambda x, y, z: (+y, -z, -x),
    lambda x, y, z: (+z, +x, +y),
    lambda x, y, z: (+z, +y, -x),
    lambda x, y, z: (+z, -x, -y),
    lambda x, y, z: (+z, -y, +x),
    lambda x, y, z: (-x, +y, -z),
    lambda x, y, z: (-x, +z, +y),
    lambda x, y, z: (-x, -y, +z),
    lambda x, y, z: (-x, -z, -y),
    lambda x, y, z: (-y, +x, +z),
    lambda x, y, z: (-y, +z, -x),
    lambda x, y, z: (-y, -x, -z),
    lambda x, y, z: (-y, -z, +x),
    lambda x, y, z: (-z, +x, -y),
    lambda x, y, z: (-z, +y, +x),
    lambda x, y, z: (-z, -x, +y),
    lambda x, y, z: (-z, -y, -x),
]


# Methods
def dist(a: tuple, b: tuple) -> float:
    return sqrt(sum(map(lambda x, y: (x - y) ** 2, a, b)))


def manhattan_dist(a: tuple, b: tuple) -> int:
    return sum(map(lambda x, y: abs(x - y), a, b))


def make_dist_dict(o: tuple, pts: set) -> dict:
    d = dict([(dist(pt, o), pt) for pt in pts])
    return d


def match_dist_dicts_by_dists(a: dict, b: dict) -> set:
    keys = set(a.keys()).intersection(set(b.keys()))
    return dict(map(lambda x: (a[x], b[x]), keys))


def match_sets_by_dists(a: set, b: set) -> dict:
    global MATCH_NUM_REQUIRED
    for oa in a:
        da = make_dist_dict(oa, a)
        for ob in b:
            db = make_dist_dict(ob, b)
            matched = match_dist_dicts_by_dists(da, db)
            if len(matched) >= MATCH_NUM_REQUIRED:
                return matched
    return None


def rotate(vec: tuple, rot: int) -> tuple:
    global VALID_ORIENTATIONS
    return VALID_ORIENTATIONS[rot](*vec)


def translate(vec: tuple, xlate: tuple) -> tuple:
    return tuple(map(sum, zip(vec, xlate)))


def diff(a: tuple, b: tuple) -> tuple:
    return tuple(map(lambda x, y: x - y, a, b))


def find_transformation(pairs: dict) -> tuple[tuple, int]:
    global VALID_ORIENTATIONS
    dst, src = zip(*pairs.items())
    for i in range(len(VALID_ORIENTATIONS)):
        rot = list(map(lambda x: rotate(x, i), src))
        off = diff(dst[0], rot[0])
        if all(map(lambda x, y: translate(x, off) == y, rot, dst)):
            return off, i
    return None


def merge_sets_by_dists(a: set, b: set) -> bool:
    match = match_sets_by_dists(a, b)
    if match is None:
        return None

    xform = find_transformation(match)
    if xform is None:
        return None

    b = set(map(lambda x: translate(rotate(x, xform[1]), xform[0]), b))
    return a.union(b), xform


# Load points
data = []
for l in read_lines_lazy('day19.txt'):
    l = l.strip()
    if l.startswith('---'):
        data.append(set())
    elif len(l) < 1:
        pass
    else:
        data[-1].add(tuple(map(int, l.split(','))))

# Distance matching to find common points (distance is invariant to both translation and rotation).
# All sets will be blended to a single one.
# Note: Assuming, that all sets have some common points! It will loop infinitely otherwise.
merged = data[0]
origins = [(0, 0, 0)]
remaining = deque(data[1:])
while remaining:
    current = remaining.popleft()
    m = merge_sets_by_dists(merged, current)
    if m is None:
        # No common points have been found yet, try again after all the others
        remaining.append(current)
    else:
        merged = m[0]
        origins.append(m[1][0])

# Get maximal manhattan distance
max_dist = 0
for i in range(len(origins)):
    for j in range(i + 1, len(origins)):
        max_dist = max(max_dist, manhattan_dist(origins[i], origins[j]))

# Print results
print("Part 1:", len(merged))
print("Part 2:", max_dist)