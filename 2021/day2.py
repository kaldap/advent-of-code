from aoc_utils import read_lines_lazy

# Part 1
x = 0
d = 0
for cmd in read_lines_lazy('day2.txt'):
    p = cmd.split()
    if p[0] == "forward":
        x += int(p[1])
    elif p[0] == "up":
        d -= int(p[1])
    elif p[0] == "down":
        d += int(p[1])

print("Part 1:", d * x)

# Part 2
x = 0
d = 0
a = 0
for cmd in read_lines_lazy('day2.txt'):
    p = cmd.split()
    if p[0] == "forward":
        x += int(p[1])
        d += a * int(p[1])
    elif p[0] == "up":
        a -= int(p[1])
    elif p[0] == "down":
        a += int(p[1])

print("Part 2:", d * x)
