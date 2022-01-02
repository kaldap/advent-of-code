import copy
from aoc_utils import read_lines, count_elements, dict_least_most_items, merge_counts


commands = list(map(lambda x: x.strip(), read_lines('day14.txt')))
template = str(commands[0])
commands = commands[2:]

reps = {}
for cmd in commands:
    reps[cmd[0:2]] = cmd[0] + cmd[-1] + cmd[1]


def deduce(depth, s, reps, cache):
    if depth < 0:
        return count_elements(s)

    n = reps.get(s, None)
    if n is None:
        return count_elements(s)

    id = (depth, n)
    if id in cache:
        return copy.copy(cache[id])

    l = deduce(depth - 1, n[0:2], reps, cache)
    r = deduce(depth - 1, n[1:3], reps, cache)
    r[n[1]] -= 1
    res = merge_counts(l, r)
    cache[id] = res
    return copy.copy(res)


for part, steps in enumerate([10, 40]):
    result = {template[0]: 1}
    e = len(template) - 1
    i = 0
    cache = {}
    while i < e:
        x = deduce(steps - 1, template[i:i+2], reps, cache)
        x[template[i]] -= 1
        result = merge_counts(result, x)
        i += 1

    # print(result)
    L, U = dict_least_most_items(result)
    print(f"Part {part + 1}:", result[U] - result[L])



