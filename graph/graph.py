from math import sqrt
from queue import Queue
from stack import Stack

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


class SearchHandler(object):
	
	def __init__(self):
		self.visited = set()

	def onVisit(self, vertex):
		print("Visit vertex: {}".format(vertex))
		self.visited.add(vertex)

	def isVisited(self, vertex):
		return (vertex in self.visited)

	def onAdjacentAlreadyVisited(self, vertex, adjacent):
		pass

	def onAdjacentNotVisitedYet(self, vertex, adjacent):
		pass

	def postVisit(self, vertex):
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
					file.write(str(vertex1)+'-'+str(vertex2))

	def getAdjacents(self, vertex):
		return self.edges[vertex]

	def getVertices(self):
		return self.vertices

	def iterate(self, first, searchHandler, structure):
		structure.push(first)

		while not structure.empty():
			vertex = structure.pop()
			searchHandler.onVisit(vertex)

			for adjacent in self.getAdjacents(vertex):
				if searchHandler.isVisited(adjacent):
					searchHandler.onAdjacentAlreadyVisited(vertex, adjacent)
				else:
					searchHandler.onAdjacentNotVisitedYet(vertex, adjacent)
					structure.push(adjacent)

			searchHandler.postVisit(vertex)

	def breadthFirstSearch(self, first, searchHandler):
		self.iterate(first, searchHandler, Queue())

	def depthFirstSearch(self, first, searchHandler):
		self.iterate(first, searchHandler, Stack())



if __name__ == '__main__':
	graph = Graph()

	root = Vertex(1, 0)
	graph.addVertex(root)

	for x in xrange(1,10):
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

	graph.breadthFirstSearch(root, SearchHandler())
	print("--------------")
	graph.depthFirstSearch(root, SearchHandler())
