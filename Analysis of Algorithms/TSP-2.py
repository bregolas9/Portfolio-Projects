def solve_tsp(G):
    node = 0
    visited_nodes = []
    edge_cost = 0

    while node not in visited_nodes:
        edges = G[node]
        minimum_edge = -1
        minimum_node = -1
        visited_nodes.append(node)

        for j, k in enumerate(edges):
            if minimum_edge == -1 and j not in visited_nodes:
                minimum_edge = k
                minimum_node = j

            elif minimum_edge != -1 and k < minimum_edge and j not in visited_nodes:
                minimum_edge = k
                minimum_node = j

        if minimum_node != -1:
            node = minimum_node

        if minimum_edge != -1:
            edge_cost += minimum_edge

    edge_cost += G[node][0]
    print("Output:", edge_cost)
    print(visited_nodes)
