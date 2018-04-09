#coding: utf-8

USAGE = """Uso: {} EQUIPOS JUGADORES_POR_EQUIPO [DIR PRF]

EQUIPOS					el número de equipos
JUGADORES_POR_EQUIPO	el número de jugadores por equipo
DIR PRF					directorio donde buscar los archivos .prf (el actual por defecto)
""".format(__file__)

from sys import argv
from gale_shapley import *


if __name__ == '__main__':
	if len(argv) not in (3, 4):
		print(USAGE)
		exit(1)

	number_of_teams, number_of_players_per_team = int(argv[1]), int(argv[2])
	number_of_players = number_of_teams * number_of_players_per_team

	prf_dir = '.'
	if len(argv) == 4:
		prf_dir = argv[3]

	players = []
	for player_id in range(1, number_of_players + 1):
		with open("{}/jugador_{}.prf".format(prf_dir, player_id)) as f:
			prefs = [int(t) for t in f.readlines()]
			print(prefs)
			players.append(Player(player_id, prefs))

	teams = []
	for team_id in range(1, number_of_teams + 1):
		with open("{}/equipo_{}.prf".format(prf_dir, team_id)) as f:
			teams.append(Team(team_id, [int(p) for p in f.readlines()], number_of_players_per_team))

	gs = GaleShapley(teams, players)
	gs.solve()
	print(gs.get_teams())
