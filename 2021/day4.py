from copy import deepcopy
from aoc_utils import read_lines


class Bingo:
    def __init__(self, board):
        self.dim = len(board), len(board[0])
        self.board = board
        self.marked = []
        self.dict = {}
        self.last_draw = -1
        for i in range(len(board)):
            self.marked.append([False] * len(board[i]))
            for j in range(len(board[i])):
                self.dict[board[i][j]] = (i, j)

    def check_win(self):
        for i in range(self.dim[0]):
            if all(self.marked[i]):
                return True
        for i in range(self.dim[1]):
            if all([x[i] for x in self.marked]):
                return True
        return False

    def draw(self, num):
        self.last_draw = num
        pos = self.dict.get(num, None)
        if pos:
            self.marked[pos[0]][pos[1]] = True
        return self.check_win()

    def score(self):
        sum = 0
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                if not self.marked[i][j]:
                    sum += self.board[i][j]
        return sum * self.last_draw


##############################################################
lines = [l.strip() for l in read_lines('day4.txt')]
seq = [int(x) for x in lines[0].split(',')]
lines_per_board = 6
boards = []

for ix in range(2, len(lines), lines_per_board):
    b_lines = [[int(y) for y in x.split()] for x in lines[ix:ix+5]]
    boards.append(Bingo(b_lines))

res = None
all_res = []
prev = [False] * len(boards)
for num in seq:
    r = [b.draw(num) for b in boards]
    if any(r):
        if not res:
            res = deepcopy(r)
        passed = [(i, boards[i].score()) for i in filter(lambda x: x >= 0, [(i if r[i] and not prev[i] else -1) for i in range(len(r))])]
        if any(passed):
            all_res.append(passed)
        prev = r

scores = all_res[0]
max_score = max([s[1] for s in scores])
max_score = list(filter(lambda x: x[1] == max_score, scores))

print("Wins", max_score[0][0], "with", max_score[0][1], "points")
assert len(all_res[-1]) == 1, "Too many loosers!"
print("Losts", all_res[-1][0][0], "with", all_res[-1][0][1], "points")