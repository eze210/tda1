from dynamic import print_level, run_simulation, solve_game


def left_shift(tup, n):
    if not tup or not n:
        return tup
    n %= len(tup)
    return tup[n:] + tup[:n]


def build_dmg_grid(dmg_grid, ship_positions):
    new_grid = []
    for pos, row in zip(ship_positions, dmg_grid):
        new_grid.append(left_shift(row, pos))
    return new_grid


def solve_positions(D, dmg_grid, hitpoints, num_shots, ship_positions):
    num_ships = len(hitpoints)
    num_cols = len(dmg_grid[0])
    if num_ships == len(ship_positions):
        dmg_grid = build_dmg_grid(dmg_grid, ship_positions)
        points, _ = solve_game(dmg_grid, hitpoints, num_shots)
        return points, ship_positions

    best_score, best_positions = 0, tuple()
    for i in range(num_ships - len(ship_positions)):
        for j in range(num_cols):
            new_score, new_positions = solve_positions(D, dmg_grid, hitpoints, num_shots, ship_positions + tuple([j]))
            if new_score > best_score:
                best_score, best_positions = new_score, new_positions
    return best_score, best_positions


def get_ship_positions(dmg_grid, hitpoints, num_shots):
    """Finds the initial ship positions that would maximize the adversary's points."""

    D = {}
    return solve_positions(D, dmg_grid, hitpoints, num_shots, tuple())[1]



if __name__ == '__main__':
    # creates a test level
    level = [
        [10, 30, 800, 1],
        [400, 400, 50, 100],
        [300, 200, 100, 300],
    ]
    ships_health = [800, 800, 800]
    print_level(ships_health, level)
    shots_per_turn = 2

    # finds the solution
    solution = solve_game(level, ships_health, shots_per_turn)
    print()
    print('points:', solution[0])
    print('shot sequence:', solution[1])
    print()

    # finds the worst case
    positions = get_ship_positions(level, ships_health, shots_per_turn)
    new_grid = build_dmg_grid(level, positions)
    print_level(ships_health, new_grid)
    solution = solve_game(new_grid, ships_health, shots_per_turn)
    print()
    print()
    print('ship positions')
    print(positions)
    print()
    print('points:', solution[0])
    print('shot sequence:', solution[1])
    print()

    # runs and shows the game using the obtained solution
    run_simulation(level, ships_health, solution[1])
