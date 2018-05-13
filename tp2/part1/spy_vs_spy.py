__doc__ = f"""
Uso: {__file__} [-h/--help] indice_espia_1 indice_espia_2 indice_aeropuerto [directorio]

indice_espia_1 Es el indice del vertice del espia 1 en un archivo de nombre mapa.coords
indice_espia_2 Es el indice del vertice del espia 2 en un archivo de nombre mapa.coords
indice_aeropuerto Es el indice del vertice del aeropuerto en un archivo de nombre mapa.coords
directorio Es el directorio en el que se debe buscar el archivo mapa.coords

mapa.coords debe tener un formato como el siguiente:

    p1.x p1.y - p2.x p2.y
    p2.x p2.y - p3.x p3.y
    p2.x p2.y - p4.x p4.y
    p4.x p4.y - p1.x p1.y

"""

from structures.graph import Graph, Vertex
from sys import argv
from bfs import BreadthFirstSearch
from dijkstra import Dijkstra




def buildGraph(file_name, spy1_index=0, spy2_index=1, airport_index=2, real_distance=False):
    g = Graph(real_distance=real_distance)
    spy1_vertex = None
    spy2_vertex = None
    airport_vertex = None

    with open(file_name, "r") as file:
        cur_index = 0
        for line in file:
            coord = line.split('-')
            coord1 = coord[0].split()
            coord2 = coord[1].split()

            vertex1 = Vertex(int(coord1[0]), int(coord1[1]))
            vertex2 = Vertex(int(coord2[0]), int(coord2[1]))

            if cur_index == spy1_index:
                spy1_vertex = vertex1
            if cur_index == spy2_index:
                spy2_vertex = vertex1
            if cur_index == airport_index:
                airport_vertex = vertex1

            g.addVertex(vertex1)
            g.addVertex(vertex2)

            if (real_distance):
                g.addEdge(vertex1, vertex2, vertex1.distance(vertex2))
            else:
                g.addEdge(vertex1, vertex2, 1)
            
            cur_index += 1

    assert spy1_vertex != None, "Spy 1 vertex not found"
    assert spy2_vertex != None, "Spy 2 vertex not found"
    assert airport_vertex != None, "Airport vertex not found"

    return g, spy1_vertex, spy2_vertex, airport_vertex

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
    if '-h' in argv or '--help' in argv:
        print(__doc__)
        exit(0)
    elif len(argv) == 4:
        directory = "."
    elif len(argv) == 5:
        directory = argv[4]
    else:
        print(__doc__)
        exit(1)

    spy1_index, spy2_index, airport_index = int(argv[1]), int(argv[2]), int(argv[3])
    print("Item 1:")
    mapGraph, spy1_vertex, spy2_vertex, airport_vertex = buildGraph(file_name="./{dir}/mapa.coords".format(dir=directory))
    spyVsSpy(mapGraph, airportVertex=airport_vertex, spy1Vertex=spy1_vertex, spy2Vertex=spy2_vertex)
    print("")

    print("Item 2:")
    mapGraph, spy1_vertex, spy2_vertex, airport_vertex = buildGraph(file_name="./{dir}/mapa.coords".format(dir=directory), real_distance=True)
    spyVsSpyWithDistances(mapGraph, airportVertex=airport_vertex, spy1Vertex=spy1_vertex, spy2Vertex=spy2_vertex)
    print("")

    print("Item 3:")
    mapGraph, spy1_vertex, spy2_vertex, airport_vertex = buildGraph(file_name="./{dir}/mapa.coords".format(dir=directory))
    spyVsSpyShortestPath(mapGraph, airportVertex=airport_vertex, spy1Vertex=spy1_vertex, spy2Vertex=spy2_vertex)
    print("")

    print("Item 4:")
    mapGraph, spy1_vertex, spy2_vertex, airport_vertex = buildGraph(file_name="./{dir}/mapa.coords".format(dir=directory), real_distance=True)
    spyVsSpyShortestPathWithDistances(mapGraph, airportVertex=airport_vertex, spy1Vertex=spy1_vertex, spy2Vertex=spy2_vertex)
