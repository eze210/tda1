from collections import defaultdict

def get_shoots(shots, boats, c=None):
    if shots == 0:
        yield c
        return

    for i in range(boats):
        p = c or [0] * boats
        p[i] += 1
        for e in get_shoots(shots - 1, boats, p):
            yield e
        p[i] -= 1


def print_level(hitpoints, dmg_grid):
    """Prints the grid of damage in a pretty format."""

    assert len(hitpoints) == len(dmg_grid)
    for hp, row in zip(hitpoints, dmg_grid):
        print('{:3} '.format(hp), end='')
        print('[' + ', '.join('{:3}'.format(e) for e in row) + ']')


def print_hp(boats_health, hit_index, dmg, turn):
    """Pints the HP of the boats.
    `boats_health` is the current HP of each boat.
    `hit_index` the index of the boat hitted in this step.
    `dmg` the damage done to that boat.
    `turn` the current turn.
    """
    print('[', end='')
    for i, e in enumerate(boats_health):
        fmt = '{:3}'
        if i == hit_index:
            fmt = '\033[0;31m{:3}\033[0m'
        print(fmt.format(e), end=', ')
    print('] ({:3}) in turn {:2}'.format(-dmg, turn))


def run_simulation(level, boats_health, solution):
    """Given a sequence of shots, simulates and shows a step-by-step execution of the game."""

    for turn, sequence in enumerate(solution):
        for boat in sequence:
            dmg = level[boat][turn % len(level[0])]
            boats_health[boat] -= dmg
            print_hp(boats_health, boat, dmg, turn)

        alive_boats = [x for x in boats_health if x > 0]
        print('{: >35}\033[0;32m(+{})\033[0m'.format('', len(alive_boats)))


def boats_left(hitpoints, damage):
    """Returns the number of boats not destroyed.
    `hitpoints` the total HP of the boats.
    `damage` accumulated damage for each boat.
    """
    count = 0
    for hp, dmg in zip(hitpoints, damage):
        if hp > dmg:
            count += 1
    return count


def hit_boat(D, dmg, dmg_grid, hitpoints, turn, shots_left, total_shots, seq, points):
    """Hits every boat and returns the best sequence of shots (i.e. the one that finished with
    less points).

    `D` is the cache of intermediate solutions.
    `dmg` is the accumulated damage so far.
    `dmg_grid` is the grid of damage points for each position.
    `hitpoints` the boats HP.
    `turn` the current turn.
    `shots_left` the number of shots left for this turn.
    `total_shots` the total number of shots allowed in a single turn.
    `seq` the sequence of boat indexes shot in the current turn.
    `points` accumulated points so far.
    """
    dmg_tuple = tuple(dmg)
    column = turn % len(dmg_grid[0])

    # if there is a better case already calculated and it's better than the current branch,
    # aborts the search because it cannot be better
    if D['best_case'] <= points:
        return float("inf"), tuple()

    # checks if this sub problem was already solved
    if len(seq) > 0 and (turn, shots_left, dmg_tuple) in D:
        return D[(column, shots_left, dmg_tuple)]

    # checks if the turn has ended or there are no more boats left
    if shots_left == 0 or boats_left(hitpoints, dmg) == 0:
        new_pts = boats_left(hitpoints, dmg)

        if new_pts > 0:
            # recursive call that solves the next turn
            pts, prev_seq = hit_boat(D, dmg, dmg_grid, hitpoints, turn + 1, total_shots, total_shots, [], points + new_pts)
            D[(column, shots_left, dmg_tuple)] = (pts, (tuple(seq),) + prev_seq)
        else:
            # if there are no more boats, this branch finished
            D[(column, shots_left, dmg_tuple)] = (points, (tuple(seq),))
            if D['best_case'] > points:
                D['best_case'] = points
        return D[(column, shots_left, dmg_tuple)]
    else:
        # this section calculates all the possible scenarios with the different shot combinations
        min_pts = float("inf")  # the points of the best intermediate solution
        min_prev_seq = None     # the sequence of shots done in that solution

        # hits every boat and gets the best intermediate solution
        for b in range(len(hitpoints)):
            # if the boat was already destroyed, skips the branch
            if dmg[b] >= hitpoints[b]:
                continue

            # appends the shot index to the current turn sequence
            seq.append(b)
            dmg[b] += dmg_grid[b][column]

            # recursive call that does another hit or steps into the next turn if no more shots available
            pts, prev_seq = hit_boat(D, dmg, dmg_grid, hitpoints, turn, shots_left - 1, total_shots, seq, points)
            if pts <= min_pts:
                min_pts = pts
                min_prev_seq = prev_seq

            # undoes the damage for the next iteration
            dmg[b] -= dmg_grid[b][turn % len(dmg_grid[0])]
            seq.pop()

        assert min_prev_seq is not None, (turn, seq)

        # stores and returns the sub problem solution
        D[(column, shots_left, dmg_tuple)] = (min_pts, min_prev_seq)
        return D[(column, shots_left, dmg_tuple)]


def solve_game(dmg_grid, hitpoints, num_shots):
    """Runs the algorithm that solves the game. The algorithm tries every possible
    combination of shots while accumulating damage for each boat until every boat is destroyed
    and then returns the sequence of shots that resulted in the minimum points.

    `dmg_grid` is the grid of damage points for each position.
    `hitpoints` the boats HP.
    `num_shots` the total number of shots allowed in a single turn.
    """
    D = defaultdict(dict)
    D['best_case'] = float('inf')
    return hit_boat(D, [0] * len(hitpoints), dmg_grid, hitpoints, 0, num_shots, num_shots, [], 0)


if __name__ == '__main__':
    # creates a test level
    level = [
        [0, 0, 35, 1, 1, 15, 20, 40],
        [10, 1, 30, 20, 10, 25, 10, 40],
        [0, 5, 20, 40, 5, 1, 20, 20],
    ]
    boats_health = [35, 105, 151]
    print_level(boats_health, level)
    shots_per_turn = 3

    # finds the solution
    solution = solve_game(level, boats_health, shots_per_turn)
    print()
    print('points:', solution[0])
    print('shot sequence:', solution[1])
    print()

    # runs and shows the game using the obtained solution
    run_simulation(level, boats_health, solution[1])
