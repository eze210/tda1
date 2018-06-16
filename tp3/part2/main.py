from structures.graph import Graph

def edge_cmp(edge1, edge2):
    weight1 = edge1[2]
    weight2 = edge2[2]

    if (weight1 > weight2):
        return 1
    if (weight1 == weight2):
        return 0

    return -1;

def maximun_capacity_edges(graph):
    vertices = graph.getVertices();
    max_capacity = -1
    max_edge = None

    for vertex1 in vertices:
        adjacents = graph.getAdjacentVertices(vertex1)
        for vertex2 in adjacents:
            edge = (vertex1, vertex2)
            capacity = graph.getEdgeWeight(vertex1, vertex2)
            if (capacity > max_capacity):
                max_capacity = capacity
                max_edge = edge

    return edge

def minimun_flow_edge(graph, source, sink):
    edges = graph.getEdges()

    max_edge = edges[0]
    edge_weight = graph.getEdgeWeight(max_edge[0], max_edge[1])
    
    graph.deleteEdge(max_edge[0], max_edge[1])
    
    min_max_flow = graph.edmonsKarp(source, sink)

    graph.addEdge(max_edge[0], max_edge[1], edge_weight)

    for i in range(1, len(edges)):
        edge = edges[i]
        edge_weight = graph.getEdgeWeight(edge[0], edge[1])
        graph.deleteEdge(edge[0], edge[1])
        max_flow = graph.edmonsKarp(source, sink)

        if (max_flow < min_max_flow):
            min_max_flow = max_flow
            max_edge = edge

        graph.addEdge(edge[0], edge[1], edge_weight)

    return max_edge

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
    g = buildGraph(file_name="./dataset/redsecreta.map")
    print(maximun_capacity_edges(g))
    print(minimun_flow_edge(g, 0, 1))



