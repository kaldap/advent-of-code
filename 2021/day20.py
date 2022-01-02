import copy
from aoc_utils import read_lines, get_neighbors_coord, iter2d

# Config
ITER_FIRST = 2
ITER_SECOND = 50


# Image class
class Image:
    lit = None
    lit_ob = False
    algo = None
    size = None
    origin = None

    def __init__(self, file):
        data = list(map(lambda s: s.strip(), read_lines(file)))
        self.algo = data[0]

        data = data[2:]
        self.size = len(data[0]), len(data)
        self.origin = 0, 0
        self.lit = set()
        for x, y in iter2d(self.size[0], self.size[1]):
            if data[y][x] == '#':
                self.lit.add((x, y))

    def num_lit(self):
        return len(self.lit)

    def is_lit(self, x, y):
        if x < self.origin[0] or \
           y < self.origin[1] or \
           x >= (self.origin[0] + self.size[0]) or \
           y >= (self.origin[1] + self.size[1]):
            return self.lit_ob
        return (x, y) in self.lit

    def filter(self):
        new_lit = set()
        neigh = ((-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
        new_origin = self.origin[0] - 1, self.origin[1] - 1
        new_size = self.size[0] + 2, self.size[1] + 2
        for coord in iter2d(new_size[0], new_size[1], new_origin[0], new_origin[1]):
            bit_str = ['0'] * len(neigh)
            for i, n in enumerate(neigh):
                test = coord[0] + n[0], coord[1] + n[1]
                if self.is_lit(*test):
                    bit_str[i] = '1'
            num = int(''.join(bit_str), 2)
            if self.algo[num] == '#':
                new_lit.add(coord)

        self.lit = new_lit
        self.origin = new_origin
        self.size = new_size

        if self.algo[0] == '#' and not self.lit_ob:
            self.lit_ob = True
        elif self.algo[-1] == '.' and self.lit_ob:
            self.lit_ob = False

    def to_string(self, l, t, w, h):
        res = ''
        for y in range(t, t+h):
            for x in range(l, l+w):
                res += '#' if self.is_lit(x, y) else '.'
            res += '\n'
        return res


# Iterate
image = Image('day20.txt')
for i in range(1, ITER_SECOND + 1):
    image.filter()
    if i == ITER_FIRST:
        print("Part 1:", image.num_lit())
print("Part 2:", image.num_lit())