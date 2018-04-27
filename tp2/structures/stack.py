from collections import deque, Iterable

class Stack(object):

	def __init__(self, **kwargs):
		self.internal = deque(**kwargs)
	
	def pop(self):
		return self.internal.pop()

	def push(self, elem):
		if not isinstance(elem, Iterable):
			return self.internal.append(elem)

		for e in elem:
			self.internal.append(e)

	def empty(self):
		return len(self) == 0

	def __len__(self):
		return len(self.internal)

	def __repr__(self):
		return 'wrapped_'+str(self.internal)