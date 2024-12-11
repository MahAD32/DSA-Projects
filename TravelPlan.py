import heapq

def shortest_path(graph, source, destination):
    pq = []
    heapq.heappush(pq, (0, source))  # (cost, node)
    costs = {node: float('inf') for node in graph}
    costs[source] = 0
    predecessors = {node: None for node in graph}

    while pq:
        current_cost, current_node = heapq.heappop(pq)

        if current_cost > costs[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            new_cost = current_cost + weight

            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (new_cost, neighbor))

    path = []
    node = destination
    while node is not None:
        path.insert(0, node)
        node = predecessors[node]

    return costs[destination], path

def main():
    graph = {
        'A': [('B', 2), ('C', 5)],
        'B': [('A', 2), ('C', 6), ('D', 1)],
        'C': [('A', 5), ('B', 6), ('D', 2)],
        'D': [('B', 1), ('C', 2), ('E', 1)],
        'E': [('D', 1)]
    }

    print("Pathfinder Tool")
    print("Available Nodes: A, B, C, D, E")

    start_node = input("Enter the starting node: ").strip().upper()
    end_node = input("Enter the ending node: ").strip().upper()

    if start_node not in graph or end_node not in graph:
        print("Invalid nodes specified.")
        return

    cost, route = shortest_path(graph, start_node, end_node)

    if cost == float('inf'):
        print(f"No path found between {start_node} and {end_node}.")
    else:
        print(f"Optimal route from {start_node} to {end_node}: {' -> '.join(route)}")
        print(f"Path cost: {cost}")

if __name__ == "__main__":
    main()
