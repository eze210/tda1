from collections import defaultdict
try:
    from math import inf as Infinite
except Exception as e:
    Infinite = float('inf')

def get_shoots(shots, boats, c=None):
	"""Calculates the shots combinations for given number of shots and boats.
	`shots` number of shots.
	`boats` number of boats.
	`c` previous result.
	"""
	if shots == 0:
		yield tuple(c)
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


def apply_shots(hitpoints, shots_combination, dmg_grid, column):
	"""Applies the damages to the hitpoints.
	`hitpoints` the total HP of the boats.
	`shots_combination` the shots combination.
	`dmg_grid` the input grid of the algorithm.
	`column` the current column in the grid.
	"""
	hitpoints = list(hitpoints)
	for boat, num_shots in enumerate(shots_combination):
		hitpoints[boat] -= dmg_grid[boat][column] * num_shots
		if hitpoints[boat] < 0:
			hitpoints[boat] = 0
	return tuple(hitpoints)


def should_ignore_shots_combination(hitpoints, shots_combination):
	"""Applies some rules to ignore the irrelevant combinations.
	`hitpoints` the total HP of the boats.
	`shots_combination` the shots combination.
	"""
	# avoid shots to zero-hp ships
	for boat, num_shots in enumerate(shots_combination):
		if hitpoints[boat] == 0 and num_shots > 0:
			return True

	# avoid repeated combinations
	sequence = combination_to_sequence(shots_combination)
	if tuple(sorted(sequence)) != sequence:
		print("Ignored ", sequence)
		return True

	return False


def count_ships(hitpoints):
	"""Counts the number of ships with hp > 0.
	`hitpoints` the current hp for each ship.
	"""
	count = 0
	for hp in hitpoints:
		if hp > 0:
			count += 1
	return count


def combination_to_sequence(combination):
	"""Translates a combination of shots to a sequence of shots.
	`combination` the shots combination.
	"""
	comb = []
	for boat, num_shots2 in enumerate(combination):
		comb += ([boat] * num_shots2)
	return tuple(comb)


def recursive_solve(D, dmg_grid, hitpoints, num_shots, turn, points_in_turn):
	"""Recursive function that solves the problem."""
	column = turn % len(dmg_grid[0])
	num_boats = len(dmg_grid)

	# checks if the current branch is a very bad solution
	if D['best_case'] < points_in_turn:
		# return a very bad answer
		return Infinite, tuple()

	# checks if this sub problem was already solved
	if (column, hitpoints) in D:
		return D[(column, hitpoints)]

	# base case (all ships are dead)
	if count_ships(hitpoints) == 0:
		# update the best case
		if points_in_turn < D['best_case']:
			D['best_case'] = points_in_turn

		# return the base solution
		return (0, tuple())

	# inits the solution for the current turn
	best_points = Infinite
	best_sequence = tuple()
	best_solution_future = tuple()

	# iterates over all shots combinations for the current turn
	for shots_combination in get_shoots(num_shots, num_boats):
		# checks some rules to ignore useless shots
		if should_ignore_shots_combination(hitpoints, shots_combination):
			continue

		# calculates the hitpoints that will have the ships in the next turn
		combination_hitpoints = apply_shots(hitpoints, shots_combination, dmg_grid, column)

		# recursively calls the same function for the next turn
		combination_points, solution_future = recursive_solve(	D,
																dmg_grid,
																combination_hitpoints,
																num_shots,
																turn + 1,
																points_in_turn + count_ships(combination_hitpoints))

		# saves the minimum
		if combination_points <= best_points:
			best_points = combination_points
			best_sequence = combination_to_sequence(shots_combination)
			best_solution_future = solution_future

	# saves the sub problem in a memory
	subproblem_points = best_points + count_ships(hitpoints)
	subproblem_sequence = (best_sequence,) + best_solution_future
	if subproblem_points < Infinite:
		D[(column, hitpoints)] = (subproblem_points, subproblem_sequence)
	return (subproblem_points, subproblem_sequence)


def solve_game(dmg_grid, hitpoints, num_shots):
	"""Runs the algorithm that solves the game. The algorithm tries every possible
	combination of shots while accumulating damage for each boat until every boat is destroyed
	and then returns the sequence of shots that resulted in the minimum points.

	`dmg_grid` is the grid of damage points for each position.
	`hitpoints` the boats HP.
	`num_shots
	` the total number of shots allowed in a single turn.
	"""
	D = defaultdict(dict)
	D['best_case'] = Infinite
	return recursive_solve(D, dmg_grid, tuple(hitpoints), num_shots, 0, 0)


if __name__ == '__main__':
	# creates a test level
	level = [
		[10, 30, 800, 1],
		[400, 400, 50, 100],
		[100, 100, 100, 100],
	]
	boats_health = [800, 800, 800]
	print_level(boats_health, level)
	shots_per_turn = 1

	# finds the solution
	solution = solve_game(level, boats_health, shots_per_turn)
	print()
	print('points:', solution[0])
	print('shot sequence:', solution[1])
	print()

	# runs and shows the game using the obtained solution
	run_simulation(level, boats_health, solution[1])
