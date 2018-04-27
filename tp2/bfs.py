from structures.graph import SearchHandler, defaultGraph
from structures.queue import Queue


class BFSSearchHandler(SearchHandler):

	def __init__(self):
		super(BFSSearchHandler, self).__init__()
		self.visited = set()

	def onVisit(self, vertex):
		print("Visit vertex: {}".format(vertex))
		self.visited.add(vertex)

	def shouldPushAdjacent(self, vertex, adjacent):
		return adjacent not in self.visited

	def getStructure(self):
		return Queue()

if __name__ == '__main__':
	graph, root = defaultGraph()
	graph.iterate(root, BFSSearchHandler())

