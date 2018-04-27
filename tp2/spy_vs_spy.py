from structures.graph import Graph, Vertex
from plot import Plotter
from sys import argv
from bfs import BFSSearchHandler


def spyVsSpy(mapGraph=None, airportVertex=None, spy1Vertex=None, spy2Vertex=None):
    Plotter(mapGraph).plot()
    bfs = BFSSearchHandler()
    mapGraph.iterate(spy1Vertex, bfs)
    mapGraph.iterate(spy2Vertex, bfs)


if __name__ == '__main__':
    mapGraph = Graph(file_name="./{dir}/mapa.coords".format(dir=argv[1]))
    spyVsSpy(mapGraph, airportVertex=Vertex(50, 50), spy1Vertex=Vertex(1, 1), spy2Vertex=Vertex(10, 10))
