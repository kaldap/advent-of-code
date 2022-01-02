#ROOMS_P1 = [[1, 0], [2, 3], [1, 2], [3, 0]]
ROOMS_P1 = [[2, 3], [2, 3], [0, 1], [1, 0]]
ROOMS_P2 = [[3, 3], [2, 1], [1, 0], [0, 2]]


class GameState:

    def __init__(self, state):
        self.room_depth = (len(state) - 11) // 4
        self.hall_index = 4 * self.room_depth
        self.junctions = [self.hall_index + 2 * x for x in range(1, 5)]
        self.state = tuple(state)

    @staticmethod
    def from_rooms(rooms):
        state = tuple(rooms[0]) + tuple(rooms[1]) + tuple(rooms[2]) + tuple(rooms[3]) + (11 * (-1,))
        return GameState(state)

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def __str__(self):
        # return \
        #     '#############\n' + \
        #     '#' + ''.join(map(GameState.get_tile_char, self.state[8:])) + '#\n' + \
        #     '###' + '#'.join(map(GameState.get_tile_char, self.state[0:8:2])) + '###\n' + \
        #     '  #' + '#'.join(map(GameState.get_tile_char, self.state[1:8:2])) + '#  \n' + \
        #     '  #########   \n'
        return str(self.state)

    @staticmethod
    def get_tile_char(tile_value):
        return '.' if tile_value < 0 else chr(ord('A') + tile_value)

    def is_empty(self, tile):
        return self.state[tile] < 0

    def get_move(self, src, dst):
        state = list(self.state)
        state[src], state[dst] = state[dst], state[src]
        return GameState(state)

    def get_reachable_tiles(self, src):
        if self.is_empty(src):
            # Nothing to move here
            return []

        if src >= self.hall_index:
            # In the hallway -> go home
            room_dst = self.state[src]
            hall_dst = 2 * room_dst + self.junctions[0]
            hall = range(hall_dst, src) if hall_dst < src else range(src + 1, hall_dst + 1)
            if not all(map(self.is_empty, hall)):
                # Someone is blocking the hallway
                return []

            room_dst *= self.room_depth
            target_ix = None
            empty = True
            for ix in range(room_dst, room_dst + self.room_depth):
                if empty:
                    if self.is_empty(ix):
                        target_ix = ix
                        continue
                    empty = False
                if self.state[ix] != self.state[src]:
                    # Someone still does not belong to this room
                    return []

            # If free space found and everybody belong here, return the position
            return [target_ix] if target_ix is not None else []

        # In the room -> move out
        room_id = src // self.room_depth
        room_start = self.room_depth * room_id
        if (src % self.room_depth) > 0:
            if not all(map(self.is_empty, range(room_start, src))):
                # Way out of the room is blocked
                return []

        if (src % self.room_depth) <= (self.room_depth - 1):
            if all(map(lambda tile: self.state[tile] == room_id, range(src, room_start + self.room_depth))):
                # We (src and all below) are home already
                return []

        junction = 2 * (src // self.room_depth) + self.junctions[0]
        targets = []

        # Test all moves to the left
        for i in range(junction, self.hall_index - 1, -1):
            if self.is_empty(i):
                if i not in self.junctions:
                    targets.append(i)
            else:
                break

        # Test all moves to the right
        for i in range(junction + 1, len(self.state)):
            if self.is_empty(i):
                if i not in self.junctions:
                    targets.append(i)
            else:
                break

        return targets

    def get_cost(self, src, dst):
        cost = 10 ** self.state[src]
        distance = 0
        if src < self.hall_index:
            distance += (src % self.room_depth) + 1
            src = 2 * (src // self.room_depth) + self.junctions[0]
        if dst < self.hall_index:
            distance += (dst % self.room_depth) + 1
            dst = 2 * (dst // self.room_depth) + self.junctions[0]
        distance += abs(src - dst)
        return max(0, distance * cost)

    def get_all_moves(self):
        for src in range(len(self.state)):
            for dst in self.get_reachable_tiles(src):
                yield self.get_move(src, dst), self.get_cost(src, dst)


def solve(state, target, history, in_cost):
    prev_cost = history.get(state, None)
    if prev_cost is not None and in_cost >= prev_cost:
        # This state has been already visited with better cost, stop the recursion.
        return None

    if state == target:
        # Find the target state. No more steps -> zero cost
        return in_cost

    # Iterate over possible moves and remember the best ones
    best = None
    history[state] = in_cost

    all_moves = list(state.get_all_moves())
    all_moves.sort(key=lambda x: x[1])

    for new_state, cost in all_moves:
        result = solve(new_state, target, history, in_cost + cost)
        if result is not None:
            if best is None or best > result:
                best = result

    # Clean up & return the best score
    return best


# Merge P1 to P2
for i in range(len(ROOMS_P1)):
    ROOMS_P2[i] = ROOMS_P1[i][0:1] + ROOMS_P2[i] + ROOMS_P1[i][1:]

# Solve
INITIAL_STATE_P1 = GameState.from_rooms(ROOMS_P1)
INITIAL_STATE_P2 = GameState.from_rooms(ROOMS_P2)
TARGET_STATE_P1 = GameState.from_rooms([[0, 0], [1, 1], [2, 2], [3, 3]])
TARGET_STATE_P2 = GameState.from_rooms([[0, 0, 0, 0], [1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]])
print("Part 1:", solve(INITIAL_STATE_P1, TARGET_STATE_P1, {}, 0))
print("Part 2:", solve(INITIAL_STATE_P2, TARGET_STATE_P2, {}, 0))
