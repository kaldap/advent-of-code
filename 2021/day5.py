from aoc_utils import read_lines, sign
import numpy as np

lines = [[int(x) for x in l.replace(' -> ', ',').strip().split(',')] for l in read_lines('day5.txt')]
b_size = max([max(l) for l in lines]) + 1
counts = np.zeros((b_size, b_size))
counts_non_diag = np.zeros((b_size, b_size))

for l in lines:
    if l[0] == l[2]:
        for y in range(min(l[1], l[3]), max(l[1], l[3]) + 1):
            counts[l[0]][y] += 1
            counts_non_diag[l[0]][y] += 1
    elif l[1] == l[3]:
        for x in range(min(l[0], l[2]), max(l[0], l[2]) + 1):
            counts[x][l[1]] += 1
            counts_non_diag[x][l[1]] += 1
    else:
        delta_x = l[2] - l[0]
        delta_y = l[3] - l[1]
        sx = sign(delta_x)
        sy = sign(delta_y)
        x = l[0]
        y = l[1]
        for i in range(abs(delta_x) + 1):
            counts[x][y] += 1
            x += sx
            y += sy

print("Part 1:", np.count_nonzero(counts_non_diag >= 2))
print("Part 2:", np.count_nonzero(counts >= 2))

