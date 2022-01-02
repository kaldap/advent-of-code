#PAWNS = (4, 8)
PAWNS = (9, 4)
BOARD_SIZE = 10
FINAL_SCORE = 21

# How many universes will produce the same outcome
# (There are 27 different rolls but only 9 outcomes)
OUTCOMES = dict([(x, 0) for x in range(3, 10)])
for i in range(1, 4):
    for j in range(1, 4):
        for k in range(1, 4):
            OUTCOMES[i+j+k] += 1

# Explore the game tree
UNIVERSES = [0, 0]  # In how many universes will the player win


def turn(player, positions, scores, universes, roll=0):
    global OUTCOMES
    global BOARD_SIZE
    global FINAL_SCORE
    global UNIVERSES

    for steps, count in OUTCOMES.items():
        pos = positions[player]
        pos += steps
        if pos > BOARD_SIZE:
            pos -= BOARD_SIZE

        score = scores[player] + pos
        end = (score >= FINAL_SCORE)
        if end:
            UNIVERSES[player] += universes * count
            continue

        if player == 0:
            turn(1, (pos, positions[1]), (score, scores[1]), universes * count, roll + 3)
        else:
            turn(0, (positions[0], pos), (scores[0], score), universes * count, roll + 3)


turn(0, PAWNS, (0, 0), 1)
print("Player 1:", UNIVERSES[0])
print("Player 2:", UNIVERSES[1])
print("Part 2 solution:", max(UNIVERSES))