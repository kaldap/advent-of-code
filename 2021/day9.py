from collections import deque
from aoc_utils import read_lines, get_neighbors, iter2d, get_neighbors_coord


def risk_level(m, coord):
    return 1 + int(m[coord[1]][coord[0]])


def find_basin(m, coord):
    solved = set()
    open = deque([coord])
    while open:
        curr = open.popleft()
        solved.add(curr)
        risk = risk_level(m, curr)
        nbs = get_neighbors_coord(m, curr[0], curr[1])
        for nb in nbs:
            if nb in solved:
                continue
            rl = risk_level(m, nb)
            if risk < rl < 10:
                open.append(nb)
    return list(solved)


heightmap = [x.strip() for x in read_lines('day9.txt')]
low_pts = list(filter(lambda coord: all(map(lambda h: h is None or h > heightmap[coord[1]][coord[0]], get_neighbors(heightmap, coord[0], coord[1]).values())), iter2d(len(heightmap[0]), len(heightmap))))
risks = list(map(lambda x: risk_level(heightmap, x), low_pts))
total_risk = sum(risks)
basins = list(map(lambda x: len(find_basin(heightmap, x)), low_pts))
basins.sort(reverse=True)

print("Part 1:", total_risk)
print("Part 2:", basins[0] * basins[1] * basins[2])
