class Team(object):
	"""Class representing a basketball team"""

	def __init__(self, name, preferences, max_players_num = 10):
		self.name = name
		self.preferences = preferences
		self.players = set()
		self.next_player_index = 0
		self.max_players_num = max_players_num

	def has_place(self):
		return len(self.players) < self.max_players_num

	def add_player(self, player):
		self.players.add(player)

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
		return str(self.name)
