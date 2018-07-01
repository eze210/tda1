from structures.graph import Graph, MaxFlowEdge
from heapq import heappush, heappop

def maximum_capacity_edge(graph):
    vertices = graph.getVertices()
    max_capacity = -1
    max_edge = None

    for vertex1 in vertices:
        adjacents = graph.getAdjacentVertices(vertex1)
        for vertex2 in adjacents:
            capacity = graph.getEdgeWeight(vertex1, vertex2)
            if (capacity > max_capacity):
                max_capacity = capacity
                max_edge = (vertex1, vertex2)

    return max_edge

def minimum_flow_edge(graph, source, sink):
    edges = graph.getEdges()

    max_edge = edges[0]
    edge_weight = graph.getEdgeWeight(max_edge[0], max_edge[1])
    
    graph.deleteEdge(max_edge[0], max_edge[1])
    
    min_max_flow = graph.edmonsKarp(source, sink)

    graph.addEdge(max_edge[0], max_edge[1], edge_weight)
    edge_heap = []

    for i in range(1, len(edges)):
        edge = edges[i]
        edge_weight = graph.getEdgeWeight(edge[0], edge[1])
        graph.deleteEdge(edge[0], edge[1])
        max_flow = graph.edmonsKarp(source, sink)
        flow_edge = MaxFlowEdge(max_flow, edge[0], edge[1])
        heappush(edge_heap, flow_edge)
        graph.addEdge(edge[0], edge[1], edge_weight)

    max_edge = heappop(edge_heap)
    second_max_edge = heappop(edge_heap)
    return [max_edge, second_max_edge]

def buildGraph(file_name):
    g = Graph()

    with open(file_name, "r") as file:
        for line in file:
            vertex1, vertex2, edge_weight = [int(i) for i in line.split()]

            g.addVertex(vertex1)
            g.addVertex(vertex2)

            g.addEdge(vertex1, vertex2, edge_weight)

    return g
            
if __name__ == '__main__':
    # Greedy algorithm
    g = buildGraph(file_name="./dataset/redsecreta.map")
    max_capacity_edge = maximum_capacity_edge(g)
    edge_weight = g.getEdgeWeight(max_capacity_edge[0], max_capacity_edge[1])
    g.deleteEdge(max_capacity_edge[0], max_capacity_edge[1])
    sec_max_capacity_edge = maximum_capacity_edge(g)
    g.addEdge(max_capacity_edge[0], max_capacity_edge[1], edge_weight)

    # Optimal algorithm
    opt_edges = minimum_flow_edge(g, 0, 1)
    opt_edge = opt_edges[0]
    second_opt_edge = opt_edges[1]

    print("Maximum flow: "+str(g.edmonsKarp(0, 1)))

    # Greedy
    edge_weight = g.getEdgeWeight(max_capacity_edge[0], max_capacity_edge[1])
    g.deleteEdge(max_capacity_edge[0], max_capacity_edge[1])
    print("Max capacity edge: "+str(max_capacity_edge))
    print("Maximum flow without max capacity edge: "+str(g.edmonsKarp(0, 1)))
    g.addEdge(max_capacity_edge[0], max_capacity_edge[1], edge_weight)

    edge_weight = g.getEdgeWeight(sec_max_capacity_edge[0], sec_max_capacity_edge[1])
    g.deleteEdge(sec_max_capacity_edge[0], sec_max_capacity_edge[1])
    print("Second max capacity edge: "+str(sec_max_capacity_edge))
    print("Maximum flow without edge: "+str(g.edmonsKarp(0, 1)))
    g.addEdge(sec_max_capacity_edge[0], sec_max_capacity_edge[1], edge_weight)

    # Optimal
    edge_weight = g.getEdgeWeight(opt_edge.vertex1, opt_edge.vertex2)
    g.deleteEdge(opt_edge.vertex1, opt_edge.vertex2)
    print("Optimal edge: ", opt_edge.vertex1, opt_edge.vertex2)
    print("Maximum flow without optimal edge: "+str(g.edmonsKarp(0, 1)))
    g.addEdge(opt_edge.vertex1, opt_edge.vertex2, edge_weight)

    edge_weight = g.getEdgeWeight(second_opt_edge.vertex1, second_opt_edge.vertex2)
    g.deleteEdge(second_opt_edge.vertex1, second_opt_edge.vertex2)
    print("Second optimal edge: ", second_opt_edge.vertex1, second_opt_edge.vertex2)
    print("Maximum flow without 2nd optimal edge: "+str(g.edmonsKarp(0, 1)))
    g.addEdge(second_opt_edge.vertex1, second_opt_edge.vertex2, edge_weight)
