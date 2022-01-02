from math import sqrt, ceil, floor

# Target rectangle definition
RECT = (153, 199, -114, -75)  # X0, X1, Y0, Y1

# Convert X to positive side (for simplicity)
x0 = min(abs(RECT[0]), abs(RECT[1]))
x1 = max(abs(RECT[0]), abs(RECT[1]))
y0 = min(RECT[2], RECT[3])
y1 = max(RECT[2], RECT[3])

# Velocity X1 is the maximal possible, faster will overshoot in single step.
# Velocity Y0 is the minimal possible, lesser will overshoot in single step.
# Maximal velocity is ~max(|Y0|,|Y1|) (larger will overshoot on return)
min_x_vel = None
max_x_vel = x1
min_y_vel = y0
max_y_vel = max(abs(y0), abs(y1)) + 1

# Find minimal horizontal velocity able to reach the target area.
dist = 0
for vel in range(1, x1 + 1):
    dist += vel
    if dist >= x0:
        min_x_vel = vel
        break

# Find all vertical velocities able to hit the target area.
# The distance is in fact the sum of arithmetic sequence (Vn=V0-n).
# The sum (distance after n steps) is: S=n*V0-(n*(n-1))/2
# Therefore steps (n) can be solved by quadratic root formula.
valid_y = []
for vel in range(max_y_vel, min_y_vel - 1, -1):
    # Using the arithmetic sequence sum formula where n=V0 (which yields Ymax=(V0^2+V0)/2)
    # (Highest point for negative velocities is reached after single step and is equal to the initial velocity)
    max_y = y = ((vel * vel + vel) // 2) if vel > 0 else vel
    steps = max(1, vel + 1)
    v = -1 if vel >= 0 else vel - 1

    # Simulate the fall (can be possibly solved by the quadratic root formula, but simulation is used for simplicity)
    while y >= y0:
        if y <= y1:
            valid_y.append((vel, max_y, y, steps))
        y += v
        steps += 1
        v -= 1

# Sort by highest reached coordinate
valid_y.sort(key=lambda x: x[1], reverse=True)
max_sim_steps = max(map(lambda x: x[3], valid_y))

# Generate dictionary of possible X velocities for each possible number of simulation steps
valid_x = dict([(x, {}) for x in range(max_sim_steps + 1)])
for vel in range(min_x_vel, x1 + 1):
    dist = v = vel
    step = 1
    while dist <= x1 and step <= max_sim_steps:
        if dist >= x0:
            valid_x[step][vel] = dist
        v = max(0, v - 1)
        step += 1
        dist += v

# Find intersection of valid X and Y velocities
all_solutions = []
distinct_solutions = {}
for y_vel, y_max, y_dist, steps in valid_y:
    x_sol = valid_x[steps]
    if not x_sol:
        continue
    for x_vel, x_dist in x_sol.items():
        key = (x_vel, y_vel)
        if key not in distinct_solutions:
            distinct_solutions[key] = len(all_solutions)
            all_solutions.append((key, (x_dist, y_dist), y_max, steps))

# Since the valid_y list has been sorted by max_y, the first solution is the best for [PART 1]
print("Part 1 solution:", all_solutions[0][2])
print("Part 2 solution:", len(distinct_solutions))