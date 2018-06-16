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
		if (not self.hasEdge()):
			raise ValueError("The edge does not exist")
		del self.edges[vertex1][vertex2]

	def updateEdgeWeight(self, vertex1, vertex2, weight):
		if (not self.hasEdge()):
			raise ValueError("The edge does not exist")
		self.edges[vertex1][vertex2] = weight

	def getEdgeWeight(self, vertex1, vertex2):
		if not vertex2 in self.edges[vertex1]:
			raise ValueError("The edge does not exist")

		return self.edges[vertex1][vertex2]

	def hasEdge(self, vertex1, vertex2):
		if ((not vertex1 in self.edges) or (not vertex2 in self.edges[vertex1])):
			return False

		return True

	def dump(self, file_name):
		with open(file_name, "w") as file:
			for vertex1 in self.edges:
				for vertex2 in self.edges[vertex1]:
					file.write(str(vertex1)+' - '+str(vertex2) + '\n')

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
		residualGraph = self.copy()
		for vertex1 in self.vertices:
			for vertex2 in self.vertices[vertex1]:
				residualGraph.addVertex(vertex2, vertex1, 0)
		return residualGraph

	def _bfsEdmondsKarp(self, residualGraph, sink, fathers, M, bfsQueue):
		while (len(bfsQueue) > 0):
			u = bfsQueue.pop(0):
			for v in residualGraph.getAdjacentVertices(u):
				capacity = residualGraph.getEdgeWeight(u, v)
				residual_capacity = residualGraph.getEdgeWeight(v, u)
				if ((capacity - residual_capacity) > 0) and (not fathers[v]):
  					fathers[v] = u
  					M[v] = min(M[u], capacity - residual_capacity)
  					if v != sink:
  						bfsQueue.append(v)
  					else:
  						return M[sink], fathers
  		return 0, fathers

  	def edmonsKarp(self, source, sink):
  		residualGraph = self.createResidualGraph()
  		max_flow = 0

  		while True:
  			path = [None for x in range(len(self.vertices))]
  			M = [0 for x in range(len(self.vertices))]

  			M[source] = decimal.Decimal('Infinity')
  			bfsQueue = []
  			bfsQueue.append(source)

  			path_flow, path = self._bfsEdmondsKarp(residualGraph, sink, path, M, bfsQueue)

  			if (not path_flow):
  				break

  			max_flow += path_flow

  			v = sink
  			while sink != source:
  				u = fathers[v]
  				capacity = residualGraph.getEdgeWeight(u, v)
				residual_capacity = residualGraph.getEdgeWeight(v, u)
  				residualGraph.updateEdgeWeight(u, v, capacity - path_flow)
  				residualGraph.updateEdgeWeight(v, u, residualGraph + path_flow)
  				v = u

  		return max_flow

def defaultGraph():
	graph = Graph()

	root = Vertex(1, 0)
	graph.addVertex(root)

	for x in range(1,10):
		v = Vertex(x, 1)
		graph.addVertex(v)
		graph.addEdge(root, v, root.distance(v))
		graph.addEdge(v, root, root.distance(v))

		u = Vertex(x, 2)
		graph.addVertex(u)
		graph.addEdge(u, root, root.distance(u))
		graph.addEdge(v, u, v.distance(u))

		w = Vertex(x, 3)
		graph.addVertex(w)
		graph.addEdge(u, w, w.distance(u))

	return graph, root


if __name__ == '__main__':
	assert hash(Vertex(0, 0)) == hash(Vertex(0, 0))
	assert Vertex(0, 0) == Vertex(0, 0)
	assert (0, 0) == (0, 0)
	graph = defaultGraph()
	print(graph)
