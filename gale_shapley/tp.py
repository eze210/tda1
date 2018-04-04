from sys import argv
from gale_shapley import *

if __name__ == '__main__':
	number_of_teams, number_of_players_per_team = int(argv[1]), int(argv[2])
	number_of_players = number_of_teams * number_of_players_per_team

	players = []
	for player_id in xrange(1, number_of_players + 1):
		with open("jugador_%d.prf" % player_id) as f:
			prefs = [int(t) for t in f.readlines()]
			print prefs
			players.append(Player(player_id, prefs))

	teams = []
	for team_id in xrange(1, number_of_teams + 1):
		with open("equipo_%d.prf" % team_id) as f:
			teams.append(Team(team_id, [int(p) for p in f.readlines()], number_of_players_per_team))

	gs = GaleShapley(teams, players)
	gs.solve()
	print gs.get_teams()
