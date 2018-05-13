from structures.graph import Graph, Vertex
from sys import argv
from bfs import BreadthFirstSearch
from dijkstra import Dijkstra


def spyVsSpy(mapGraph=None, airportVertex=None, spy1Vertex=None, spy2Vertex=None):
    print("Spy 1 arrives in {} steps.".format(mapGraph.iterate(spy1Vertex, BreadthFirstSearch()).getLevel(airportVertex)))
    print("Spy 2 arrives in {} steps.".format(mapGraph.iterate(spy2Vertex, BreadthFirstSearch()).getLevel(airportVertex)))

def spyVsSpyWithDistances(mapGraph=None, airportVertex=None, spy1Vertex=None, spy2Vertex=None):
    print("Spy 1 distance: {}.".format(mapGraph.iterate(spy1Vertex, Dijkstra(mapGraph, spy1Vertex)).getDistance(airportVertex)))
    print("Spy 2 distance: {}.".format(mapGraph.iterate(spy2Vertex, Dijkstra(mapGraph, spy2Vertex)).getDistance(airportVertex)))

def spyVsSpyShortestPath(mapGraph=None, airportVertex=None, spy1Vertex=None, spy2Vertex=None):
    print("Spy 1 shortest path: {}.".format(mapGraph.iterate(spy1Vertex, BreadthFirstSearch()).getShortestPath(airportVertex)))
    print("Spy 2 shortest path: {}.".format(mapGraph.iterate(spy2Vertex, BreadthFirstSearch()).getShortestPath(airportVertex)))

def spyVsSpyShortestPathWithDistances(mapGraph=None, airportVertex=None, spy1Vertex=None, spy2Vertex=None):
    print("Spy 1 shortest path: {}.".format(mapGraph.iterate(spy1Vertex, Dijkstra(mapGraph, spy1Vertex)).getShortestPath(airportVertex)))
    print("Spy 2 shortest path: {}.".format(mapGraph.iterate(spy2Vertex, Dijkstra(mapGraph, spy2Vertex)).getShortestPath(airportVertex)))

if __name__ == '__main__':
    print("Item 1:")
    mapGraph = Graph(file_name="./{dir}/mapa.coords".format(dir=argv[1]))
    spyVsSpy(mapGraph, airportVertex=Vertex(50, 50), spy1Vertex=Vertex(1, 1), spy2Vertex=Vertex(10, 10))
    print("")

    print("Item 2:")
    mapGraph = Graph(file_name="./{dir}/mapa.coords".format(dir=argv[1]), real_distance=True)
    spyVsSpyWithDistances(mapGraph, airportVertex=Vertex(50, 50), spy1Vertex=Vertex(1, 1), spy2Vertex=Vertex(10, 10))
    print("")

    print("Item 3:")
    mapGraph = Graph(file_name="./{dir}/mapa.coords".format(dir=argv[1]))
    spyVsSpyShortestPath(mapGraph, airportVertex=Vertex(50, 50), spy1Vertex=Vertex(1, 1), spy2Vertex=Vertex(10, 10))
    print("")

    print("Item 4:")
    mapGraph = Graph(file_name="./{dir}/mapa.coords".format(dir=argv[1]), real_distance=True)
    spyVsSpyShortestPathWithDistances(mapGraph, airportVertex=Vertex(50, 50), spy1Vertex=Vertex(1, 1), spy2Vertex=Vertex(10, 10))
