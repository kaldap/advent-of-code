from copy import deepcopy
from aoc_utils import read_lines, bin_to_num

e = None
num_bits = 12
bit_count = [[0] * num_bits, [0] * num_bits]
lines = [bits.strip() for bits in read_lines('day3.txt')]
for bits in lines:
    for i, b in enumerate(bits):
        bit_count[int(b)][i] += 1

# Power
g = 0
for i in range(num_bits):
    g <<= 1
    if bit_count[0][i] < bit_count[1][i]:
        g |= 1
e = (~g) & ((2 ** num_bits) - 1)

# Oxygen generator rating
f_lines = deepcopy(lines)
for char in range(num_bits):
    bit_count = [[0] * num_bits, [0] * num_bits]
    for bits in f_lines:
        for i, b in enumerate(bits):
            bit_count[int(b)][i] += 1
    look_for = '1' if bit_count[1][char] >= bit_count[0][char] else '0'
    f_lines = list(filter(lambda x: x[char] == look_for, f_lines))
    if len(f_lines) == 1:
        break
assert len(f_lines) == 1, "Too many lines!"
ogr = bin_to_num(f_lines[0])

# CO2 scrubber
f_lines = deepcopy(lines)
char = 0
for char in range(num_bits):
    bit_count = [[0] * num_bits, [0] * num_bits]
    for bits in f_lines:
        for i, b in enumerate(bits):
            bit_count[int(b)][i] += 1
    look_for = '0' if bit_count[0][char] <= bit_count[1][char] else '1'
    f_lines = list(filter(lambda x: x[char] == look_for, f_lines))
    if len(f_lines) == 1:
        break
assert len(f_lines) == 1, "Too many lines!"
cosr = bin_to_num(f_lines[0])

print("Power (Part 1):", e * g)
print("Life Support Rating (Part 2):", ogr * cosr)
