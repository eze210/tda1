from heap import MaxHeap

class Player(object):

	def __init__(self, name, preferences):
		self.name = name
		self.preferences = preferences
		self.team = None
		self.next_team_index = 0

	def is_free(self):
		return (self.team == None)

	def set_team(self, team):
		self.team = team

	def set_free(self):
		self.team = None

	def get_next_preference(self):
		next_team = self.preferences[self.next_team_index]
		self.next_team_index += 1
		return next_team

	def try_with_next_team(self, teams_map, on_fail, on_fail_context):
		team = teams_map[self.get_next_preference()]
		team.try_add_player(self, on_fail, on_fail_context)

	def __repr__(self):
		return self.name


class Team(object):

	def compare_players(self, player1, player2):
		if self.preferences[player1.name] < self.preferences[player2.name]:
			return 1
		elif self.preferences[player1.name] == self.preferences[player2.name]:
			return 0
		else:
			return -1

	def __init__(self, name, preferences, max_players_num = 10):
		self.name = name
		self.preferences = {}
		idx = len(preferences)
		for p in preferences:
			self.preferences[p] = idx
			idx -= 1
		self.players = MaxHeap(self.compare_players)
		self.max_players_num = max_players_num

	def has_place(self):
		return self.players.size() < self.max_players_num

	def prefers(self, player):
		return self.preferences[player.name] > self.preferences[self.players.top().name]

	def try_add_player(self, player, sad_man_callback=None, callback_context=None):
		if self.has_place():
			print "Free team %s adds player %s" % (self.name, player.name)
			self.players.add(player)
			player.set_team(self.name)

		elif self.prefers(player):
			sad = self.players.pop()
			sad.set_free()

			print "Team %s changes player %s by %s" % (self.name, sad.name, player.name)
			self.players.add(player)
			player.set_team(self.name)
			if sad_man_callback != None:
				sad_man_callback(sad, callback_context)

		else:
			print "Team %s keeps player %s and rejects %s" % (self.name, self.players, player.name)
			if sad_man_callback != None:
				sad_man_callback(player, callback_context)

	def __repr__(self):
		return self.name


class GaleShapleyBasket(object):

	def __init__(self, teams, players):
		self.teams = teams
		self.players = players

	def on_sad_man(self, free_player, free_players):
		free_players.append(free_player)

	def solve(self):
		free_players = self.players
	
		teams_map = {}
		for team in self.teams:
			teams_map[team.name] = team
	
		while len(free_players) > 0:
			new_free_players = []
			for player in free_players:
				player.try_with_next_team(teams_map, self.on_sad_man, new_free_players)
	
			free_players = new_free_players
	
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

	gsb = GaleShapleyBasket(teams=[t1, t2, t3], players=[p1, p2, p3, p4, p5, p6, p7, p8, p9])
	gsb.solve()
	print gsb.get_teams()
