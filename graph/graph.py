from math import sqrt

class _Vertex(object):

	def __init__(self, coord_x, coord_y):
		self.x = coord_x
		self.y = coord_y

	def distance(self, other):
		deltax = self.x - other.x
		deltay = self.y - other.y

		return sqrt((deltax**deltax) + (deltay**deltay))

	def __str__(self):
		return str(self.x)+' '+str(self.y)


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

	def dump(self, file_name):
		with open(file_name, "w") as file:
			for vertex1 in self.edges:
				for vertex2 in self.edges[vertex1]:
					file.write(str(vertex1)+'-'+str(vertex2))
