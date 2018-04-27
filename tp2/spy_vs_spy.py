from structures.graph import Graph
from plot import Plotter
from sys import argv

def spyVsSpy(mapGraph=None, spy1Vertex=None, spy2Vertex=None):
    Plotter(mapGraph).plot()


if __name__ == '__main__':
    mapGraph = Graph(file_name="./{dir}/mapa.coords".format(dir=argv[1]))
    spyVsSpy(mapGraph)
