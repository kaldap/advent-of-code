from aoc_utils import read_lines_lazy
import bisect
import copy


class Axis:
    def __init__(self, initializer):
        self.initializer = initializer
        self.markers = []
        self.values = []

    def split(self, item):
        index = bisect.bisect(self.markers, item)
        if index == 0:
            self.markers.insert(0, item)
            self.values.insert(0, copy.deepcopy(self.initializer))
            return 0

        if self.markers[index - 1] == item:
            return index - 1

        self.markers.insert(index, item)
        self.values.insert(index, copy.deepcopy(self.values[index - 1]))
        return index

    def get_all(self):
        return list(zip(self.markers, self.values))

    def __bool__(self):
        return len(self.parts) > 0

    def __len__(self):
        return len(self.parts)

    def __getitem__(self, item):
        if not isinstance(item, slice):
            raise "Slice required!"
        a = self.split(item.start)
        b = self.split(item.stop)
        return list(zip(self.markers[a:b], self.values[a:b]))


class Space:
    def __init__(self, cuboids):
        self.x = Axis(Axis(Axis([False])))
        for on, extents in cuboids:
            X = self.x[extents[0][0]:extents[0][1]]
            for _, x in X:
                Y = x[extents[1][0]:extents[1][1]]
                for _, y in Y:
                    Z = y[extents[2][0]:extents[2][1]]
                    for _, z in Z:
                        z[0] = on

    def count_on(self, bounds=None):
        total = 0
        all_x = self.x.get_all() if bounds is None else self.x[bounds]
        for ix in range(1, len(all_x)):
            x_count = all_x[ix][0] - all_x[ix - 1][0]
            all_y = all_x[ix - 1][1].get_all() if bounds is None else all_x[ix - 1][1][bounds]
            for iy in range(1, len(all_y)):
                y_count = all_y[iy][0] - all_y[iy - 1][0]
                all_z = all_y[iy - 1][1].get_all() if bounds is None else all_y[iy - 1][1][bounds]
                for iz in range(1, len(all_z)):
                    z_count = all_z[iz][0] - all_z[iz - 1][0]
                    if all_z[iz - 1][1][0]:
                        total += x_count * y_count * z_count
        return total


space = []
for line in read_lines_lazy('day22.txt'):
    turn_on = (line[1] == 'n')
    ranges = [[int(num) + ix for ix, num in enumerate(p.split(',')[0].split('..'))] for p in line.split('=')[1:]]
    space.append((turn_on, ranges))

space = Space(space)
PART1_RANGE = (-50, 50)
print("Part 1:", space.count_on(slice(PART1_RANGE[0], PART1_RANGE[1] + 1)))
print("Part 2:", space.count_on())

