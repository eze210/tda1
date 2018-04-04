from sys import argv
from random import shuffle

if __name__ == '__main__':
	number_of_teams, number_of_players_per_team = int(argv[1]), int(argv[2])
	number_of_players = number_of_teams * number_of_players_per_team

	teams = range(1, number_of_teams + 1)
	players = range(1, number_of_players + 1)

	for player_id in xrange(1, number_of_players + 1):
		with open("jugador_%d.prf" % player_id, "w") as f:
			shuffle(teams)
			for t in teams:
				f.write("%d\n" % t)
			

	for team_id in xrange(1, number_of_teams + 1):
		with open("equipo_%d.prf" % team_id, "w") as f:
			shuffle(players)
			for p in players:
				f.write("%d\n" % p)
