from dynamic import print_level, run_simulation, solve_game


def left_shift(tup, n):
    """Given a tuple `tup` and an integer `n`, shifts all elements in `tup` `n` places
    to the left."""

    if not tup or not n:
        return tup
    n %= len(tup)
    return tup[n:] + tup[:n]


def build_dmg_grid(dmg_grid, ship_positions):
    """Given a damage grid and a list of ship initial positions, transforms `dmg_grid`
    so as if the ships were to start at the first position shifting the rows."""

    new_grid = []
    for pos, row in zip(ship_positions, dmg_grid):
        new_grid.append(left_shift(row, pos))
    return new_grid


def solve_positions(dmg_grid, hitpoints, num_shots, ship_positions, solver):
    """Returns the initial ship positions that maximize the score of the `solver`."""

    num_ships = len(hitpoints)
    num_cols = len(dmg_grid[0])

    # base case: if all ships are positioned, solves the game
    if num_ships == len(ship_positions):
        dmg_grid = build_dmg_grid(dmg_grid, ship_positions)
        points, _ = solver(dmg_grid, hitpoints, num_shots)
        rv = points, ship_positions
    else:
        best_score, best_positions = 0, tuple()

        # goes through every possible position for the n'th ship and finds the position
        # of the ships (not already positioned) that maximizes the score
        for j in range(num_cols):
            new_score, new_positions = solve_positions(dmg_grid, hitpoints, num_shots, ship_positions + tuple([j]), solver)
            if new_score > best_score:
                best_score, best_positions = new_score, new_positions
        rv = best_score, best_positions
    return rv


def get_ship_positions(dmg_grid, hitpoints, num_shots, solver):
    """Finds the initial ship positions that would maximize the adversary's points.
    `dmg_grid` is the grid of damage points for each position.
	`hitpoints` the ships HP.
	`num_shots` the total number of shots allowed in a single turn.
    `solver` an algorithm that solves the game and receives the 3 previous parameters.
    """
    return solve_positions(dmg_grid, hitpoints, num_shots, tuple(), solver)[1]


if __name__ == '__main__':
    # creates a test level
    level = [
        [10, 30, 800, 1],
        [400, 400, 50, 100],
        [300, 200, 100, 300],
    ]
    ships_health = [700, 800, 400]
    print_level(ships_health, level)
    shots_per_turn = 4

    # finds the solution
    solution = solve_game(level, ships_health, shots_per_turn)
    print()
    print('points:', solution[0])
    print('shot sequence:', solution[1])
    print()

    # finds the worst case
    positions = get_ship_positions(level, ships_health, shots_per_turn, solve_game)
    new_level = build_dmg_grid(level, positions)
    print_level(ships_health, new_level)
    solution = solve_game(new_level, ships_health, shots_per_turn)
    print()
    print()
    print('ship positions')
    print(positions)
    print()
    print('points:', solution[0])
    print('shot sequence:', solution[1])
    print()

    # runs and shows the game using the obtained solution
    run_simulation(new_level, ships_health, solution[1])
