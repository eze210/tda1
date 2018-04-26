from graph import Graph, Vertex
from heap import MaxHeap

class Infinite(object):

	def __init__(self):
		raise Exception("Infinite is not able to have instances")

	def __gt__(number):
		return True # ;)


class Dijkstra(object):

	def comparison_between_vertices(self, vertex1, vertex2):
		if self.get_distance(vertex1) < self.get_distance(vertex2):
			return 1
		elif self.get_distance(vertex1) > self.get_distance(vertex2):
			return -1
		else:
			return 0

	def __init__(self, graph, initial_vertex):
		self.graph = graph
		self.initial_vertex = initial_vertex
		
		self.distances = {}
		self.parents = {}
		self.visited = {}

		self.heap = MaxHeap(self.comparison_between_vertices)

		for vertex in graph.getVertices():
			self.distances[vertex] = Infinite
			self.parents[vertex] = None
			self.visited[vertex] = False

	def __call__(self):
		self.distances[self.initial_vertex] = 0
		self.heap.add(self.initial_vertex)

		while self.heap.size() > 0:
			vertex = self.heap.pop()
			self.visited[vertex] = True
			for v in self.graph.getAdjacents(vertex):
				if self.distances[v] > self.distances[vertex] + self.graph.getEdgeWeight(vertex, v):
					self.distances[v] = self.distances[vertex] + self.graph.getEdgeWeight(vertex, v)
					self.parents[v] = vertex
					self.heap.add(v)

		return self.distances

	def get_distance(self, vertex):
		return self.distances[vertex]

	def is_visited(self, vertex):
		return self.visited[vertex]




if __name__ == '__main__':
	assert Infinite > 5
	assert 54 < Infinite
	assert 8 != Infinite
	assert Infinite == Infinite

	graph = Graph()

	root = Vertex(1, 1)
	graph.addVertex(root)

	for x in xrange(1,10):
		v = Vertex(x, 1)
		graph.addVertex(v)
		graph.addEdge(root, v, root.distance(v))

	d = Dijkstra(graph, root)
	print(d())
