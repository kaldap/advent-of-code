from collections import deque
import numpy as np

# Input
FISH = [2, 3, 1, 3, 4, 4, 1, 5, 2, 3, 1, 1, 4, 5, 5, 3, 5, 5, 4, 1, 2, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1, 4, 1, 3, 1, 4, 1, 1, 4, 1, 3, 4, 5, 1, 1, 5, 3, 4, 3, 4, 1, 5, 1, 3, 1, 1, 1, 3, 5, 3, 2, 3, 1, 5, 2, 2, 1, 1, 4, 1, 1, 2, 2, 2, 2, 3, 2, 1, 2, 5, 4, 1, 1, 1, 5, 5, 3, 1, 3, 2, 2, 2, 5, 1, 5, 2, 4, 1, 1, 3, 3, 5, 2, 3, 1, 2, 1, 5, 1, 4, 3, 5, 2, 1, 5, 3, 4, 4, 5, 3, 1, 2, 4, 3, 4, 1, 3, 1, 1, 2, 5, 4, 3, 5, 3, 2, 1, 4, 1, 4, 4, 2, 3, 1, 1, 2, 1, 1, 3, 3, 3, 1, 1, 2, 2, 1, 1, 1, 5, 1, 5, 1, 4, 5, 1, 5, 2, 4, 3, 1, 1, 3, 2, 2, 1, 4, 3, 1, 1, 1, 3, 3, 3, 4, 5, 2, 3, 3, 1, 3, 1, 4, 1, 1, 1, 2, 5, 1, 4, 1, 2, 4, 5, 4, 1, 5, 1, 5, 5, 1, 5, 5, 2, 5, 5, 1, 4, 5, 1, 1, 3, 2, 5, 5, 5, 4, 3, 2, 5, 4, 1, 1, 2, 4, 4, 1, 1, 1, 3, 2, 1, 1, 2, 1, 2, 2, 3, 4, 5, 4, 1, 4, 5, 1, 1, 5, 5, 1, 4, 1, 4, 4, 1, 5, 3, 1, 4, 3, 5, 3, 1, 3, 1, 4, 2, 4, 5, 1, 4, 1, 2, 4, 1, 2, 5, 1, 1, 5, 1, 1, 3, 1, 1, 2, 3, 4, 2, 4, 3, 1]

# Setup
SIMULATE_DAYS = 256
FERTILE_AFTER = 2
SPAWN_DAYS = 7
FISH = np.asarray(FISH)

# Algorithm
# Hint: Instead of remembering day counters for each fish, remember fish count with same remaining days
population = []
transposed = deque([np.count_nonzero(FISH == i) for i in range(0, SPAWN_DAYS + FERTILE_AFTER)])
for day in range(SIMULATE_DAYS):
    spawners = transposed.popleft()
    transposed.append(spawners)
    transposed[SPAWN_DAYS - 1] += spawners
    population.append((day + 1, sum(transposed)))

print("Population D80:", population[79][1])
print("Population D256:", population[255][1])