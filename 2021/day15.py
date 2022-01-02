import copy
from aoc_utils import read_lines_int_matrix, dijkstra, iter2d, get_neighbors_coord, bfs_evaluate_paths

# Read file and compute size (assuming complete grid)
risks = read_lines_int_matrix('day15.txt')
start = (0, 0)
size = (len(risks[-1]), len(risks))
end = (size[0] - 1, size[1] - 1)

# Generate list of vertices (coord. tuples) and dictionary of edges {from -> [(to, distance)]}
# V = list(iter2d(size[0], size[1]))
# E = dict([(u, [(n, risks[n[1]][n[0]]) for n in get_neighbors_coord(risks, u[0], u[1])]) for u in V])

# Run Dijkstra to find the shortest path
# _, D = dijkstra(E, V, start, end)
# print("Part 1 Dijkstra:", D)

# Dijkstra is ineffective for orthogonal graphs & the path is not needed
# Using Breadth-first search is much better
D = bfs_evaluate_paths(risks, start)
print("Part 1 BFS:", D[end[1]][end[0]])

################################################################
# Bigger repeated cave (too much for dijkstra, using BFS only) #
################################################################
REPETITIONS = (5, 5)
CHANGE = 1
WRAP = 9

# Extend each line horizontally
for y in range(size[1]):
    orig = copy.copy(risks[y])
    for x in range(1, REPETITIONS[0]):
        inc = CHANGE * x
        risks[y] += [v + inc for v in orig]

# Repeat lines vertically
for y in range(size[1], size[1] * REPETITIONS[1]):
    orig = risks[y % size[1]]
    inc = (y // size[1]) * CHANGE
    risks.append([v + inc for v in orig])

# Regenerate dimensions
size = (len(risks[-1]), len(risks))
end = (size[0] - 1, size[1] - 1)

# Wrap the values
for x, y in iter2d(size[0], size[1]):
    while risks[y][x] > WRAP:
        risks[y][x] -= WRAP

# Run BFS to find the shortest path
D = bfs_evaluate_paths(risks, start)
print("Part 2 (BFS):", D[end[1]][end[0]])