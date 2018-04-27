from structures.graph import SearchHandler, defaultGraph
from structures.stack import Stack


class DFSSearchHandler(SearchHandler):

	def __init__(self):
		super(DFSSearchHandler, self).__init__()
		self.visited = set()

	def onVisit(self, vertex):
		print("Visit vertex: {}".format(vertex))
		self.visited.add(vertex)

	def shouldPushAdjacent(self, vertex, adjacent):
		return adjacent not in self.visited

	def getStructure(self):
		return Stack()


if __name__ == '__main__':
	graph, root = defaultGraph()
	graph.iterate(root, DFSSearchHandler())
