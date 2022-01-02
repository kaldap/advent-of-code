from collections import deque
from aoc_utils import read_lines, iter2d, get_neighbors_coord


GRID = [[int(x) for x in ln.strip()] for ln in read_lines('day11.txt')]


def step(grid):
    num_flashes = 0

    r = set()
    q = deque()
    for x, y in iter2d(len(grid[0]), len(grid)):
        grid[y][x] += 1
        if grid[y][x] > 9:
            q.append((x, y))

    while q:
        coord = q.popleft()
        if coord in r:
            continue
        r.add(coord)
        num_flashes += 1
        grid[coord[1]][coord[0]] = 0
        for n in get_neighbors_coord(grid, coord[0], coord[1], True):
            if n not in r:
                grid[n[1]][n[0]] += 1
                if grid[n[1]][n[0]] > 9:
                    q.append(n)

    return num_flashes


def all_flashed(grid):
    return all([all(map(lambda y: y == 0, r)) for r in grid])


total = 0
all_step = -1
for i in range(100):
    total += step(GRID)
    if all_step < 0 and all_flashed(GRID):
        all_step = i + 1

i = 100
while all_step < 0:
    i += 1
    step(GRID)
    if all_flashed(GRID):
        all_step = i

print("Part 1:", total)
print("Part 2:", all_step)
