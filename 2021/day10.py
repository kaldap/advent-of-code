from collections import deque
from aoc_utils import read_lines_lazy

PAIR_INFO = {'(': ')', '{': '}', '[': ']', '<': '>'}
SCORE_INFO = {')': 3, ']': 57, '}': 1197, '>': 25137}
CSCORE_INFO = {')': 1, ']': 2, '}': 3, '>': 4}


def corruption_score(line):
    global PAIR_INFO
    global SCORE_INFO
    stack = deque()
    for c in line:
        if c in PAIR_INFO:
            stack.append(c)
        else:
            popped = stack.pop()
            if PAIR_INFO[popped] == c:
                continue
            if c in SCORE_INFO:
                return SCORE_INFO[c]
            return 0
    return -1


def repair_incomplete(line):
    global PAIR_INFO
    global CSCORE_INFO
    stack = deque()
    for c in line:
        if c in PAIR_INFO:
            stack.append(c)
        else:
            # It already passed the check, so just pop
            popped = stack.pop()

    score = 0
    while stack:
        c = PAIR_INFO[stack.pop()]
        line += c
        score = (score * 5) + CSCORE_INFO[c]
    return line, score


total_corr_score = 0
comp_scores = []
for l in read_lines_lazy('day10.txt'):
    l = l.strip()
    s = corruption_score(l)

    # Corrupted
    if s >= 0:
        total_corr_score += s
        continue

    # Incomplete
    _, s = repair_incomplete(l)
    comp_scores.append(s)
comp_scores.sort()

print("Part 1:", total_corr_score)
print("Part 2:", comp_scores[len(comp_scores) // 2])
