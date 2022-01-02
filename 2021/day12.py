from aoc_utils import read_lines_lazy, find_all_paths

# Build graph
graph = {}
for l in read_lines_lazy('day12.txt'):
    l = l.strip()
    nodes = l.split('-')
    if nodes[0] in graph:
        graph[nodes[0]].append(nodes[1])
    else:
        graph[nodes[0]] = [nodes[1]]
    if nodes[1] in graph:
        graph[nodes[1]].append(nodes[0])
    else:
        graph[nodes[1]] = [nodes[0]]

# Explore graph (revisit large only)
paths = find_all_paths(graph, revisit_rule=lambda n, p: n[0].isupper())
print("Part 1:", len(paths))


# Revisit one small cave twice
def stupid_revisiting_rule(node, path):
    # Start and end cannot be revisited
    if node == 'start' or node == 'end':
        return False
    if not node[0].islower():
        return True

    # Find small cave duplicates
    c = 0
    d = set()
    for cave in path:
        if not cave[0].islower():
            continue
        if cave in d:
            return False
        d.add(cave)
    return True


paths = find_all_paths(graph, revisit_rule=stupid_revisiting_rule)
print("Part 2:", len(paths))