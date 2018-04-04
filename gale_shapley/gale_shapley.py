from team import Team
from player import Player

class GaleShapley(object):

	def __init__(self, teams, players):
		self.teams = teams
		self.players = players

	def on_rejected_team(self, team, teams_with_space):
		teams_with_space.add(team)

	def solve(self):
		teams_with_space = self.teams
	
		players_map = {}
		for player in self.players:
			players_map[player.name] = player
	
		while len(teams_with_space) > 0:
			new_teams_with_space = set()
			for team in teams_with_space:
				team.try_with_next_players(players_map, self.on_rejected_team, new_teams_with_space)
	
			teams_with_space = new_teams_with_space
	
	def get_teams(self):
		return [(team.players, team) for team in self.teams]


if __name__ == '__main__':
	p1 = Player(1, [1, 2, 3])
	p2 = Player(2, [1, 2, 3])
	p3 = Player(3, [1, 2, 3])
	p4 = Player(4, [1, 2, 3])
	p5 = Player(5, [1, 2, 3])
	p6 = Player(6, [1, 2, 3])
	p7 = Player(7, [1, 2, 3])
	p8 = Player(8, [1, 2, 3])
	p9 = Player(9, [1, 2, 3])

	t1 = Team(1, [9, 2, 3, 4, 5, 6, 7, 8, 1], 3)
	t2 = Team(2, [1, 2, 3, 4, 5, 6, 7, 8, 9], 3)
	t3 = Team(3, [1, 2, 3, 4, 5, 6, 7, 8, 9], 3)

	gsb = GaleShapley(teams=[t2, t3, t1], players=[p1, p2, p3, p4, p5, p6, p7, p8, p9])
	gsb.solve()
	print gsb.get_teams()
