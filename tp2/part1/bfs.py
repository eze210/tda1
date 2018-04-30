from structures.graph import SearchHandler, defaultGraph
from structures.queue import Queue
from collections import defaultdict


class BFSSearchHandler(SearchHandler):

	def __init__(self):
		super(BFSSearchHandler, self).__init__()
		self.visited = set()
		self.parents = defaultdict(None)
		self.levels = defaultdict(lambda: 0)

	def onVisit(self, vertex):
		self.visited.add(vertex)

	def shouldPushAdjacent(self, vertex, adjacent):
		return adjacent not in self.visited
	
	def prePushAdjacent(self, vertex, adjacent):
		if adjacent not in self.parents:
			self.parents[adjacent] = vertex
			self.levels[adjacent] = self.levels[vertex] + 1

	def getStructure(self):
		return Queue()
	
	def getLevel(self, vertex):
		return self.levels[vertex]

	def getShortestPath(self, vertex):
		if vertex not in self.parents:
			return [vertex]

		path = self.getShortestPath(self.parents[vertex])
		path.append(vertex)
		return path


if __name__ == '__main__':
	graph, root = defaultGraph()
	graph.iterate(root, BFSSearchHandler())
