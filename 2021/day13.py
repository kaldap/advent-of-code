from aoc_utils import read_lines_lazy
import numpy as np


class Paper:
    points = None
    folds = 0

    def __init__(self):
        self.points = set()

    def add(self, pt):
        self.points.add(pt)

    def fold_x(self, x):
        self.folds += 1
        two_x = 2 * x
        keys = list(self.points)
        for pt in keys:
            if pt[0] > x:
                self.points.remove(pt)
                self.points.add((two_x - pt[0], pt[1]))

    def fold_y(self, y):
        self.folds += 1
        two_y = 2 * y
        keys = list(self.points)
        for pt in keys:
            if pt[1] > y:
                self.points.remove(pt)
                self.points.add((pt[0], two_y - pt[1]))

    def size(self):
        s = [-1, -1]
        for pt in self.points:
            s[0] = max(s[0], pt[0])
            s[1] = max(s[1], pt[1])
        return s[0] + 1, s[1] + 1

    def draw(self):
        s = self.size()
        img = np.zeros((s[1], s[0]))
        for pt in self.points:
            img[pt[1]][pt[0]] = 1
        for y in range(s[1]):
            for x in range(s[0]):
                print('.' if img[y][x] == 0 else '#', end='')
            print()
        print()

    def num_folds(self):
        return self.folds

    def num_dots(self):
        return len(self.points)


num_after_first = 0
pap = Paper()
for l in read_lines_lazy('day13.txt'):
    l = l.strip()
    if ',' in l:
        p = l.split(',')
        pap.add((int(p[0]), int(p[1])))
    elif 'x=' in l:
        p = l.split('=')
        pap.fold_x(int(p[1]))
        if pap.num_folds() == 1:
            num_after_first = pap.num_dots()
    elif 'y=' in l:
        p = l.split('=')
        pap.fold_y(int(p[1]))
        if pap.num_folds() == 1:
            num_after_first = pap.num_dots()


print("Part 1:", num_after_first)
print("-" * pap.size()[0])
print("Part 2:")
pap.draw()