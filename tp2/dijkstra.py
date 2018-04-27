from structures.graph import Graph, Vertex, SearchHandler
from structures.heap import MaxHeap


class Infinite(object):

	def __gt__(self, number):
		return True # ;)


class Dijkstra(SearchHandler):

	def __init__(self, graph, initial_vertex):
		super(Dijkstra, self).__init__()
		self.graph = graph
		self.initial_vertex = initial_vertex

		self.distances = {}
		self.parents = {}

		for vertex in graph.getVertices():
			self.distances[vertex] = Infinite()
			self.parents[vertex] = None

	def __call__(self):
		self.distances[self.initial_vertex] = 0
		self.graph.iterate(self.initial_vertex, self)
		return self.distances

	def getDistance(self, vertex):
		return self.distances[vertex]

	def prePushAdjacent(self, vertex, adjacent):
		super(Dijkstra, self).prePushAdjacent(vertex, adjacent)
		self.distances[adjacent] = self.distances[vertex] + self.graph.getEdgeWeight(vertex, adjacent)
		self.parents[adjacent] = vertex
		
	def shouldPushAdjacent(self, vertex, adjacent):
		return self.distances[adjacent] > self.distances[vertex] + self.graph.getEdgeWeight(vertex, adjacent)

	def getStructure(self):
		return MaxHeap(self.comparisonBetweenVertices)

	def getShortestPath(self, vertex):
		if vertex == None:
			return []

		path = self.getShortestPath(self.parents[vertex])
		path.append(vertex)
		return path

	def comparisonBetweenVertices(self, vertex1, vertex2):
		if self.getDistance(vertex1) < self.getDistance(vertex2):
			return 1
		elif self.getDistance(vertex1) > self.getDistance(vertex2):
			return -1
		else:
			return 0


if __name__ == '__main__':
	assert Infinite() > 5
	assert 54 < Infinite()
	assert 8 != Infinite()
	assert Infinite() != Infinite()

	graph = Graph()
	root = Vertex(1, 1)
	graph.addVertex(root)

	vertex = None
	for x in range(1,10):
		vertex = Vertex(x, 1)
		graph.addVertex(vertex)
		graph.addEdge(root, vertex, root.distance(vertex))

	dijkstra = Dijkstra(graph, root)
	print(dijkstra())

	print(dijkstra.getShortestPath(vertex))
