from heap import MaxHeap

class Player(object):

	def __init__(self, name, preferences):
		self.name = name
		self.preferences = {}
		idx = len(preferences)
		for p in preferences:
			self.preferences[p] = idx
			idx -= 1
		self.team = None

	def is_free(self):
		return (self.team == None)

	def prefers(self, team):
		return self.preferences[team.name] > self.preferences[self.team.name]

	def try_set_team(self, team, rejected_team_callback=None, callback_context=None):
		if self.is_free():
			print "Free player %s goes to team %s" % (self.name, team.name)
			self.team = team
			team.add_player(self.name)

		elif self.prefers(team):
			rejected = self.team
			rejected.remove_player(self.name)

			print "Player %s changes team %s by %s" % (self.name, rejected.name, team.name)
			self.team = team
			team.add_player(self.name)
			if rejected_team_callback != None:
				rejected_team_callback(rejected, callback_context)

		else:
			print "Player %s keeps team %s and rejects %s" % (self.name, self.team.name, team.name)
			if rejected_team_callback != None:
				rejected_team_callback(team, callback_context)

	def __repr__(self):
		return self.name


class Team(object):

	def __init__(self, name, preferences, max_players_num = 10):
		self.name = name
		self.preferences = preferences
		self.players = []
		self.next_player_index = 0
		self.max_players_num = max_players_num

	def has_place(self):
		return len(self.players) < self.max_players_num

	def add_player(self, player):
		self.players.append(player)

	def remove_player(self, player):
		self.players.remove(player)

	def get_next_preference(self):
		next_player = self.preferences[self.next_player_index]
		self.next_player_index += 1
		return next_player

	def try_with_next_players(self, players_map, on_fail, on_fail_context):
		while self.has_place():
			player = players_map[self.get_next_preference()]
			player.try_set_team(self, on_fail, on_fail_context)

	def __repr__(self):
		return self.name


class GaleShapleyBasket(object):

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
	p1 = Player('p1', ['t1', 't2', 't3'])
	p2 = Player('p2', ['t1', 't2', 't3'])
	p3 = Player('p3', ['t1', 't2', 't3'])
	p4 = Player('p4', ['t1', 't2', 't3'])
	p5 = Player('p5', ['t1', 't2', 't3'])
	p6 = Player('p6', ['t1', 't2', 't3'])
	p7 = Player('p7', ['t1', 't2', 't3'])
	p8 = Player('p8', ['t1', 't2', 't3'])
	p9 = Player('p9', ['t1', 't2', 't3'])

	t1 = Team('t1', ['p9', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p1'], 3)
	t2 = Team('t2', ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9'], 3)
	t3 = Team('t3', ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9'], 3)

	gsb = GaleShapleyBasket(teams=[t2, t3, t1], players=[p1, p2, p3, p4, p5, p6, p7, p8, p9])
	gsb.solve()
	print gsb.get_teams()
