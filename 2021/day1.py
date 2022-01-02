from aoc_utils import read_lines_int_lazy, sliding_window

for part in range(2):
    rising = 0
    prev = None
    window = 3**part

    for depth in sliding_window(read_lines_int_lazy('day1.txt'), window):
        if len(depth) < window:
            continue

        depth = sum(depth)
        if prev and depth > prev:
            rising += 1
        prev = depth

    print(f"Part {part + 1}:", rising)
