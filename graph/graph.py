class Graph(object):

	def __init__(self):
		self.vertices = []
		self.edges = {}

	def addVertex(self, vertex):
		self.vertices.append(vertex)

	def addEdge(self, vertex1, vertex2, weight):
		if (not ((vertex1 in self.vertices) and (vertex2 in self.vertices))):
			raise ValueError("One of the vertices is not in the graph")
		if (not vertex1 in self.edges):
			self.edges[vertex1] = {}
		self.edges[vertex1][vertex2] = weight

	def getEdgeWeight(self, vertex1, vertex2):
		if ((not vertex1 in self.edges) or (not vertex2 in self.edges[vertex1])):
			raise ValueError("The edge does not exist")
		return self.edges[vertex1][vertex2]

	def hasEdge(self, vertex1, vertex2):
		if ((not vertex1 in self.edges) or (not vertex2 in self.edges[vertex1])):
			return False
		return True

