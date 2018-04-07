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
			print(f"Free player {self.name} goes to team {team.name}")
			self.team = team
			team.add_player(self.name)

		elif self.prefers(team):
			rejected = self.team
			rejected.remove_player(self.name)

			print(f"Player {self.name} changes team {rejected.name} by {team.name}")
			self.team = team
			team.add_player(self.name)
			if rejected_team_callback != None:
				rejected_team_callback(rejected, callback_context)

		else:
			print(f"Player {self.name} keeps team {self.team.name} and rejects {team.name}")
			if rejected_team_callback != None:
				rejected_team_callback(team, callback_context)

	def __repr__(self):
		return str(self.name)
