import decimal

class Graph(object):

	def __init__(self, real_distance = False):
		self.vertices = []
		self.edges = {}

	def addVertex(self, vertex):
		if not vertex in self.vertices:
			self.vertices.append(vertex)
			self.edges[vertex] = {}

	def addEdge(self, vertex1, vertex2, weight):
		if (not ((vertex1 in self.vertices) and (vertex2 in self.vertices))):
			raise ValueError("One of the vertices is not in the graph")
		self.edges[vertex1][vertex2] = weight		

	def deleteEdge(self, vertex1, vertex2):
		if (not self.hasEdge(vertex1, vertex2)):
			raise ValueError("The edge does not exist")
		del self.edges[vertex1][vertex2]

	def updateEdgeWeight(self, vertex1, vertex2, weight):
		if (not self.hasEdge(vertex1, vertex2)):
			raise ValueError("The edge does not exist")
		if (not weight):
			del self.edges[vertex1][vertex2]
		else:
			self.edges[vertex1][vertex2] = weight

	def getEdgeWeight(self, vertex1, vertex2):
		if not vertex2 in self.edges[vertex1]:
			raise ValueError("The edge does not exist")

		return self.edges[vertex1][vertex2]

	def hasEdge(self, vertex1, vertex2):
		if ((not vertex1 in self.edges) or (not vertex2 in self.edges[vertex1])):
			return False

		return True

	def getAdjacents(self, vertex):
		return self.edges[vertex]

	def getAdjacentVertices(self, vertex):
		return self.edges[vertex].keys()

	def getVertices(self):
		return self.vertices

	def getEdges(self):
		edges = []
		for vertex1 in self.edges:
			for vertex2 in self.edges[vertex1]:
				edges.append((vertex1, vertex2))
		return edges

	def copy(self):
		newGraph = Graph()
		newGraph.vertices = self.vertices[:]
		newGraph.edges = dict(self.edges)
		return newGraph

	def createResidualGraph(self):
		residualGraph = Graph()
		for vertex1 in self.vertices:
			for vertex2 in self.edges[vertex1]:
				residualGraph.addVertex(vertex1)
				residualGraph.addVertex(vertex2)
				residualGraph.addEdge(vertex1, vertex2, self.getEdgeWeight(vertex1, vertex2))
				residualGraph.addEdge(vertex2, vertex1, 0)
		return residualGraph

	def _bfsEdmondsKarp(self, residualGraph, source, sink, parent):
		bfsQueue = []
		bfsQueue.append(source)
		visited = [False for x in range(len(self.vertices))]
		visited[source] = True

		while (len(bfsQueue) > 0):
			u = bfsQueue.pop(0)
			for v in residualGraph.getAdjacentVertices(u):
				capacity = residualGraph.getEdgeWeight(u, v)
				if (capacity > 0) and (not visited[v]):
					parent[v] = u
					visited[v] = True
					bfsQueue.append(v)

		return visited[sink]

	def edmonsKarp(self, source, sink):
		residualGraph = self.createResidualGraph()
		max_flow = 0
		path = [None for x in range(len(self.vertices))]

		while self._bfsEdmondsKarp(residualGraph, source, sink, path):
			path_flow = decimal.Decimal('Infinity')

			v = sink
			while v != source:
				path_flow = min(path_flow, residualGraph.getEdgeWeight(path[v], v))
				v = path[v]

			max_flow +=  path_flow

			v = sink
			while v != source:
				u = path[v]
				capacity = residualGraph.getEdgeWeight(u, v)
				residual_capacity = residualGraph.getEdgeWeight(v, u)
				residualGraph.updateEdgeWeight(u, v, capacity - path_flow)
				residualGraph.updateEdgeWeight(v, u, residual_capacity + path_flow)
				v = u
		return max_flow
