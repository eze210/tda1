class Man(object):

	def __init__(self, name, preferences):
		self.name = name
		self.preferences = preferences
		self.woman = None
		self.next_woman_index = 0

	def is_free(self):
		return (self.woman == None)

	def set_woman(self, woman):
		self.woman = woman

	def set_free(self):
		self.woman = None

	def get_next_preference(self):
		next_woman = self.preferences[self.next_woman_index]
		self.next_woman_index += 1
		return next_woman

	def __repr__(self):
		return self.name


class Woman(object):

	def __init__(self, name, preferences):
		self.name = name
		self.preferences = {}
		idx = len(preferences)
		for p in preferences:
			self.preferences[p] = idx
			idx -= 1
		self.man = None

	def is_free(self):
		return (self.man == None)

	def try_set_man(self, man):
		if self.is_free():
			print "Free woman %s engages man %s" % (self.name, man.name)
			self.man = man
			man.set_woman(self.name)
			return None

		elif self.preferences[man.name] > self.preferences[self.man.name]:
			sad = self.man
			sad.set_free()

			print "Woman %s changes man %s by %s" % (self.name, sad.name, man.name)
			self.man = man
			man.set_woman(self.name)
			return sad

		else:
			print "Woman %s keeps man %s and rejects %s" % (self.name, self.man.name, man.name)
			return man

	def __repr__(self):
		return self.name


class GaleShapley(object):

	def __init__(self, women, men):
		self.women = women
		self.men = men

	def solve(self):
		free_men = self.men
	
		women_map = {}
		for woman in self.women:
			women_map[woman.name] = woman
	
		while len(free_men) > 0:
			new_free_men = []
			for man in free_men:
				woman = women_map[man.get_next_preference()]
				sad = woman.try_set_man(man)
				if sad != None:
					new_free_men.append(sad)
	
			free_men = new_free_men
	
	def get_couples(self):
		return [(w.man, w) for w in self.women]



if __name__ == '__main__':
	w1 = Woman('w1', ['m1', 'm2', 'm3'])
	w2 = Woman('w2', ['m1', 'm2', 'm3'])
	w3 = Woman('w3', ['m1', 'm2', 'm3'])

	m1 = Man('m1', ['w1', 'w2', 'w3'])
	m2 = Man('m2', ['w1', 'w2', 'w3'])
	m3 = Man('m3', ['w1', 'w2', 'w3'])
	
	gs1 = GaleShapley(women = [w3, w2, w1],
					  men = [m1, m3, m2])
	
	w1 = Woman('w1', ['m1', 'm2'])
	w2 = Woman('w2', ['m2', 'm1'])

	m1 = Man('m1', ['w2', 'w1'])
	m2 = Man('m2', ['w1', 'w2'])

	gs2 = GaleShapley(women = [w1, w2],
				 	  men = [m1, m2])

	gs1.solve()
	print gs1.get_couples()
	print
	print
	gs2.solve()
	print gs2.get_couples()
	print
	print
	
