from structures.graph import Graph, Vertex
from plot import Plotter
from sys import argv
from bfs import BFSSearchHandler
from dijkstra import Dijkstra


def spyVsSpy(mapGraph=None, airportVertex=None, spy1Vertex=None, spy2Vertex=None):
    print("Spy 1 arrives in {} steps.".format(mapGraph.iterate(spy1Vertex, BFSSearchHandler()).getLevel(airportVertex)))
    print("Spy 2 arrives in {} steps.".format(mapGraph.iterate(spy2Vertex, BFSSearchHandler()).getLevel(airportVertex)))

def spyVsSpyWithDistances(mapGraph=None, airportVertex=None, spy1Vertex=None, spy2Vertex=None):
    print("Spy 1 distance: {}.".format(mapGraph.iterate(spy1Vertex, Dijkstra(mapGraph, spy1Vertex)).getDistance(airportVertex)))
    print("Spy 2 distance: {}.".format(mapGraph.iterate(spy2Vertex, Dijkstra(mapGraph, spy2Vertex)).getDistance(airportVertex)))


if __name__ == '__main__':
    mapGraph = Graph(file_name="./{dir}/mapa.coords".format(dir=argv[1]))
    spyVsSpy(mapGraph, airportVertex=Vertex(50, 50), spy1Vertex=Vertex(1, 1), spy2Vertex=Vertex(10, 10))

    mapGraph = Graph(file_name="./{dir}/mapa.coords".format(dir=argv[1]), real_distance=True)
    spyVsSpyWithDistances(mapGraph, airportVertex=Vertex(50, 50), spy1Vertex=Vertex(1, 1), spy2Vertex=Vertex(10, 10))
