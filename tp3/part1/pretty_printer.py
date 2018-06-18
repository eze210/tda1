
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
	print("Pretty print:")

	for turn, sequence in enumerate(solution):
		for boat in sequence:
			dmg = level[boat][turn % len(level[0])]
			boats_health[boat] -= dmg
			print_hp(boats_health, boat, dmg, turn)

		alive_boats = [x for x in boats_health if x > 0]
		print('{: >35}\033[0;32m(+{})\033[0m'.format('', len(alive_boats)))

