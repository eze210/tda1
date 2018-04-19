from sys import argv
from random import shuffle

USAGE = """Uso: {} EQUIPOS JUGADORES_POR_EQUIPO [DIR PRF]

EQUIPOS					el número de equipos
JUGADORES_POR_EQUIPO	el número de jugadores por equipo
DIR PRF					directorio donde generar los archivos .prf (el actual por defecto). Este directorio debe existir previamente.
""".format(__file__)


if __name__ == '__main__':
	if len(argv) not in (3, 4):
		print(USAGE)
		exit(1)

	number_of_teams, number_of_players_per_team = int(argv[1]), int(argv[2])
	number_of_players = number_of_teams * number_of_players_per_team

	prf_dir = '.'
	if len(argv) == 4:
		prf_dir = argv[3]

	teams = list(range(1, number_of_teams + 1))
	players = list(range(1, number_of_players + 1))

	for player_id in range(1, number_of_players + 1):
		with open("%s/jugador_%d.prf" % (prf_dir, player_id), "w") as f:
			shuffle(teams)
			for t in teams:
				f.write("%d\n" % t)


	for team_id in range(1, number_of_teams + 1):
		with open("%s/equipo_%d.prf" % (prf_dir, team_id), "w") as f:
			shuffle(players)
			for p in players:
				f.write("%d\n" % p)
