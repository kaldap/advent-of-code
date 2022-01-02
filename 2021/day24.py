###############################
# The code can be split into 14 similar sections with three varying constants (A,B,C):
#    1: inp w
#    2: mul x 0
#    3: add x z
#    4: mod x 26
#    5: div z 1  (A - 1 or 26 only)
#    6: add x 10 (B - "random" integer)
#    7: eql x w
#    8: eql x 0
#    9: mul y 0
#   10: add y 25
#   11: mul y x
#   12: add y 1
#   13: mul z y
#   14: mul y 0
#   15: add y w
#   16: add y 2 (C - "random" integer)
#   17: mul y x
#   18: add z y
# Note:
#   It is not obvious at first, but the [Z] variable simulates the stack of digits in base-26.
#   [div Z 26] simulates the POP operation, [mod Z 26] simulates the PEEK operation.
#   [mul Z 26] simulates the PUSH operation (zero is pushed, then [add Z 0..25] has to be done for changing the number).
#
# Computation:
#   The character is read first into [W] (line 1) and is not changed afterwards until next character.
#   Lines 2-4 are the PEEK op - the top of the [Z] stack is stored into [X].
#   Line 5 either keeps or removes the top of the [Z] stack. ([Z div 1] does nothing, [Z div 26] does POP).
#   Lines 6-8 are comparing the [top of the stack plus B] with the last read input character [W].
#     *  X then contains either 0 ([top + B == W]) or 1 ([top + B != W])
#   Lines 9-12 makes [Y]=[25*X+1]. Y then contains either 1 or 26 depending on [X].
#   Line 13 multiplies [Z] by [Y], so it either does nothing or PUSHes 0 to the [Z] stack.
#   Lines 14-17 makes [Y]=[X*(W+C)]. Since [X] is either 0 or 1, then [Y] is either 0 or [W+C].
#   Line 18 adds [Y] to [Z].
#
# Keypoints (to notice when inspecting the code):
#   1) [Z] simulates the stack.
#   2) There are same number of sections where [A]==1 as where [A]==26.
#   3) If [A]==1 then [B] is always generated "large enough" to force PUSHing [input + C].
#   4) If [A]==26 then [B] is always generated negative, allowing to balance the equation for [X] (lines 2-4, 6-8).
#   5) Only [A]==26 POPs.
#   6) To make [Z] zeroed, there should be equal amount of PUSH & POP ops.
#   7) When [A]==26, it must not PUSH. So the equation has to be balanced.
#
# Solution:
#   1) Push [C] and its index when [A]==1.
#   2) Pop previous [C] & modify the input to satisfy the equation.

from collections import deque
from aoc_utils import read_lines

# Variables
sums = {}
z_stack = deque()
lines = read_lines('day24.txt')

# Read input by 18 lines (one section)
for ix in range(0, len(lines), 18):
    section = ix // 18
    A = int(lines[ix + 4].split()[2])
    if A == 1:
        # Push [C]
        z_stack.append((section, int(lines[ix + 15].split()[2])))
    elif A == 26:
        # Remember character index (key) & sum of current [B] with popped [C]
        prev_sec, prev_C = z_stack.pop()
        sums[section] = (prev_sec, prev_C + int(lines[ix + 5].split()[2]))
    else:
        raise Exception("Unexpected value for A!")

# Prepare output strings
num_sections = len(lines) // 18
PART_1 = [9] * num_sections
PART_2 = [1] * num_sections

# Change the necessary positions
for ix, (prev_ix, value) in sums.items():
    if value < 0:
        # We need to make the current input smaller to balance the equation (or the other way around for PT2).
        PART_1[ix] = 9 + value
        PART_2[prev_ix] = 1 - value
    else:
        # We need to make the previous input larger to balance the equation (or the other way around for PT2).
        PART_1[prev_ix] = 9 - value
        PART_2[ix] = 1 + value

# Print the results
print("Part 1:", ''.join(map(str, PART_1)))
print("Part 2:", ''.join(map(str, PART_2)))
