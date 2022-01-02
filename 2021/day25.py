from aoc_utils import read_lines_lazy


# def draw(m, w, h):
#     for y in range(h):
#         for x in range(w):
#             if (x, y) in m[0]:
#                 print('>', end='')
#             elif (x, y) in m[1]:
#                 print('v', end='')
#             else:
#                 print('.', end='')
#         print()


# Load map
MAP = [{}, {}]
W = H = 0
for y, l in enumerate(read_lines_lazy('day25.txt')):
    l = l.strip()
    W = max(W, len(l))
    H += 1
    for x, c in enumerate(l):
        if c == '>':
            MAP[0][(x, y)] = True
        elif c == 'v':
            MAP[1][(x, y)] = True

# Iterate
PRINT_EACH = 100
MOD = [lambda x, y: ((x + 1) % W, y), lambda x, y: (x, (y + 1) % H)]
STEP = 0
MOVES = 1
while MOVES > 0:
    MOVES = 0
    STEP += 1
    if STEP % PRINT_EACH == 0:
        print("Step", STEP)
        # draw(MAP, W, H)
        # print()

    for i, mod in enumerate(MOD):
        new_map = {}
        for x, y in MAP[i].keys():
            coord = mod(x, y)
            if all(map(lambda d: coord not in d, MAP)):
                # Target empty, move
                new_map[coord] = True
                MOVES += 1
            else:
                # Target full, stay
                new_map[(x, y)] = True
        MAP[i] = new_map

print("Stopped after", STEP, "steps...")

