from math import sqrt


class Vertex(object):

	def __init__(self, coord_x, coord_y):
		self.x = coord_x
		self.y = coord_y

	def distance(self, other):
		deltax = self.x - other.x
		deltay = self.y - other.y
		return sqrt((deltax**2) + (deltay**2))

	def __str__(self):
		return str(self.x)+' '+str(self.y)

	def __repr__(self):
		return 'V(' + str(self) + ')'

	def __hash__(self):
		return hash((self.x, self.y))

	def __eq__(self, other):
		return hash(self) == hash(other)


class SearchHandler(object):
	
	def __init__(self):
		pass

	def onVisit(self, vertex):
		print("Visit vertex: {}".format(vertex))

	def onAdjacent(self, vertex, adjacent):
		pass

	def shouldPushAdjacent(self, vertex, adjacent):
		pass

	def prePushAdjacent(self, vertex, adjacent):
		pass

	def postPushAdjacent(self, vertex, adjacent):
		pass

	def postVisit(self, vertex):
		pass

	def getStructure(self):
		pass


class Graph(object):

	def __init__(self, file_name = "", real_distance = False):
		self.vertices = []
		self.edges = {}

		if file_name:
			with open(file_name, "r") as file:
				for line in file:
					coord = line.split('-')
					coord1 = coord[0].split()
					coord2 = coord[1].split()

					vertex1 = Vertex(int(coord1[0]), int(coord1[1]))
					vertex2 = Vertex(int(coord2[0]), int(coord2[1]))

					self.addVertex(vertex1)
					self.addVertex(vertex2)

					if (real_distance):
						self.addEdge(vertex1, vertex2, vertex1.distance(vertex2))
					else:
						self.addEdge(vertex1, vertex2, 1)

	def addVertex(self, vertex):
		if not vertex in self.vertices:
			self.vertices.append(vertex)
			self.edges[vertex] = {}

	def addEdge(self, vertex1, vertex2, weight):
		if (not ((vertex1 in self.vertices) and (vertex2 in self.vertices))):
			raise ValueError("One of the vertices is not in the graph")

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

	def getVertices(self):
		return self.vertices

	def iterate(self, first, searchHandler):
		structure = searchHandler.getStructure()
		structure.push(first)

		while not structure.empty():
			vertex = structure.pop()
			searchHandler.onVisit(vertex)

			for adjacent in self.getAdjacents(vertex):
				searchHandler.onAdjacent(vertex, adjacent)
				if searchHandler.shouldPushAdjacent(vertex, adjacent):
					searchHandler.prePushAdjacent(vertex, adjacent)
					structure.push(adjacent)
					searchHandler.postPushAdjacent(vertex, adjacent)
					
			searchHandler.postVisit(vertex)


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
