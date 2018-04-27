from structures.graph import Graph, Vertex
from plot import Plotter
from sys import argv
from bfs import BFSSearchHandler


def spyVsSpy(mapGraph=None, airportVertex=None, spy1Vertex=None, spy2Vertex=None):
    print("Spy 1 arrives in {} steps.".format(mapGraph.iterate(spy1Vertex, BFSSearchHandler()).getLevel(airportVertex)))
    print("Spy 2 arrives in {} steps.".format(mapGraph.iterate(spy2Vertex, BFSSearchHandler()).getLevel(airportVertex)))


if __name__ == '__main__':
    mapGraph = Graph(file_name="./{dir}/mapa.coords".format(dir=argv[1]))
    spyVsSpy(mapGraph, airportVertex=Vertex(50, 50), spy1Vertex=Vertex(1, 1), spy2Vertex=Vertex(10, 10))
