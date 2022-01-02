PAWNS = (9, 4)
#PAWNS = (4, 8)


class DeterministicDie:
    state = 0
    num_rolls = 0

    def roll(self):
        self.num_rolls += 1
        self.state += 1
        if self.state > 100:
            self.state = 1
        return self.state

    def multi_roll(self, count):
        return [self.roll() for _ in range(count)]


class Game:
    BOARD_SIZE = 10
    FINAL_SCORE = 1000

    die = None
    players = None
    score = [0, 0]
    player = 0
    end = False

    def __init__(self, state, die):
        self.players = list(state)
        self.die = die

    def turn(self):
        if self.end:
            return self.end

        dice = self.die.multi_roll(3)
        pos = self.players[self.player]
        pos += sum(dice) % self.BOARD_SIZE
        while pos > self.BOARD_SIZE:
            pos -= self.BOARD_SIZE
        self.players[self.player] = pos
        self.score[self.player] += pos
        self.end = self.score[self.player] >= self.FINAL_SCORE
        if not self.end:
            self.player = (self.player + 1) % 2
        return self.end

    def get_winner(self):
        return (self.player, self.score[self.player]) if self.end else None

    def get_looser(self):
        player = (self.player + 1) % 2
        return (player, self.score[player]) if self.end else None

    def get_rolls(self):
        return self.die.num_rolls


# Part 1
game = Game(PAWNS, DeterministicDie())
while not game.turn():
    continue
print("Part 1:", game.get_rolls() * game.get_looser()[1])


