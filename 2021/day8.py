from itertools import permutations
from aoc_utils import read_lines_lazy


def apply_mapping(x, m):
    s = list(map(lambda l: str(m[int(l)]), x))
    s.sort()
    return ''.join(s)


##############################
segments = {'abcefg': 0, 'cf': 1, 'acdeg': 2, 'acdfg': 3, 'bcdf': 4, 'abdfg': 5, 'abdefg': 6, 'acf': 7, 'abcdefg': 8, 'abcdfg': 9}
possible_mappings = list(permutations(range(7)))

##############################
char_map = list(enumerate('abcdefg'))
for n, c in char_map:
    segments = dict({(k.replace(c, str(n)), v) for k, v in segments.items()})

##############################
numbers = []
counts = dict({(i, 0) for i in range(8)})
for pattern in read_lines_lazy('day8.txt'):
    for n, c in char_map:
        pattern = pattern.replace(c, str(n))
    pattern = [x.strip() for x in pattern.split('|')]
    wiring = pattern[0].split()
    digits = pattern[1].split()
    wiring.sort(key=lambda x: len(x))
    for d in digits:
        counts[len(d)] += 1

    ##############################
    found = None
    for m in possible_mappings:
        decoded = [apply_mapping(x, m) for x in wiring]
        if all(map(lambda x: x in segments, decoded)):
            found = m
            break
    numbers.append(int(''.join([str(segments[apply_mapping(num, found)]) for num in digits])))

##############################
print("Unique digits (Part 1):", counts[2] + counts[3] + counts[4] + counts[7])
print("Sum (Part 2):", sum(numbers))