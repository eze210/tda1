from collections import defaultdict
from pretty_printer import run_simulation, print_level
try:
    from math import inf as Infinite
except Exception as e:
    Infinite = float('inf')

def get_shoots(shots, ships, c=None):
	"""Calculates the shots combinations for given number of shots and ships.
	`shots` number of shots.
	`ships` number of ships.
	`c` previous result.
	"""
	if shots == 0:
		yield tuple(c)
		return

	for i in range(ships):
		p = c or [0] * ships
		p[i] += 1
		for e in get_shoots(shots - 1, ships, p):
			yield e
		p[i] -= 1


def ships_left(hitpoints, damage):
	"""Returns the number of ships not destroyed.
	`hitpoints` the total HP of the ships.
	`damage` accumulated damage for each ship.
	"""
	count = 0
	for hp, dmg in zip(hitpoints, damage):
		if hp > dmg:
			count += 1
	return count


def apply_shots(hitpoints, shots_combination, dmg_grid, column):
	"""Applies the damages to the hitpoints.
	`hitpoints` the total HP of the ships.
	`shots_combination` the shots combination.
	`dmg_grid` the input grid of the algorithm.
	`column` the current column in the grid.
	"""
	hitpoints = list(hitpoints)
	for ship, num_shots in enumerate(shots_combination):
		hitpoints[ship] -= dmg_grid[ship][column] * num_shots
		if hitpoints[ship] < 0:
			hitpoints[ship] = 0
	return tuple(hitpoints)


def should_ignore_shots_combination(hitpoints, shots_combination):
	"""Applies some rules to ignore the irrelevant combinations.
	`hitpoints` the total HP of the ships.
	`shots_combination` the shots combination.
	"""
	# avoid shots to zero-hp ships
	for ship, num_shots in enumerate(shots_combination):
		if hitpoints[ship] == 0 and num_shots > 0:
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
	for ship, num_shots2 in enumerate(combination):
		comb += ([ship] * num_shots2)
	return tuple(comb)


def recursive_solve(D, dmg_grid, hitpoints, num_shots, turn, points_in_turn):
	"""Recursive function that solves the problem."""
	column = turn % len(dmg_grid[0])
	num_ships = len(dmg_grid)

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
	best_hitpoints = hitpoints

	# iterates over all shots combinations for the current turn
	for shots_combination in get_shoots(num_shots, num_ships):
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
			best_hitpoints = combination_hitpoints

	# saves the sub problem in a memory
	subproblem_points = best_points + count_ships(best_hitpoints)
	subproblem_sequence = (best_sequence,) + best_solution_future
	if subproblem_points < Infinite:
		D[(column, hitpoints)] = (subproblem_points, subproblem_sequence)
	return (subproblem_points, subproblem_sequence)


def solve_game(dmg_grid, hitpoints, num_shots):
	"""Runs the algorithm that solves the game. The algorithm tries every possible
	combination of shots while accumulating damage for each ship until every ship is destroyed
	and then returns the sequence of shots that resulted in the minimum points.

	`dmg_grid` is the grid of damage points for each position.
	`hitpoints` the ships HP.
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
	ships_health = [800, 800, 800]
	print_level(ships_health, level)
	shots_per_turn = 1

	# finds the solution
	solution = solve_game(level, ships_health, shots_per_turn)
	print()
	print('points:', solution[0])
	print('shot sequence:', solution[1])
	print()

	# runs and shows the game using the obtained solution
	run_simulation(level, ships_health, solution[1])
