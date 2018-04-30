import matplotlib.pyplot as plt

try:
	from networkx import nx
except ImportError as e:
	print('Please, run "sudo -H pip3 install networkx cairocffi"')
	raise e


class Plotter(object):
	"""docstring for Plotter"""
	def __init__(self, graph):
		self.graph = graph

	def plot(self):
		drawableGraph = nx.DiGraph()
		drawableGraph.add_nodes_from(self.graph.vertices)
		for v in self.graph.vertices:
			adjs = self.graph.edges[v]
			for a in adjs:
				drawableGraph.add_edge(v, a)

		plt.subplot(111)
		nx.draw(drawableGraph, with_labels=True, node_color='blue', node_size=50, width=1)
		plt.show()
