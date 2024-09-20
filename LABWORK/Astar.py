from queue import PriorityQueue

def a_star_search(graph, start, goal, heuristics):
    # Priority Queue to store nodes to be explored, with their f(n) value
    open_list = PriorityQueue()
    open_list.put((0, start))  # Initialize with the start node

    # Dictionary to keep track of the path
    came_from = {}

    # Dictionary to store the cost from the start node to each node
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0  # Cost from start to start is zero

    # Dictionary to store the total cost (g + h) for each node
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristics[start]  # f(n) = h(n) for the start node

    while not open_list.empty():
        # Get the node with the lowest f(n) value
        current = open_list.get()[1]

        # If the goal is reached, reconstruct the path
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]  # Return reversed path

        # Explore neighbors of the current node
        for neighbor, weight in graph[current].items():
            # Calculate tentative g score for the neighbor
            tentative_g_score = g_score[current] + weight

            # If this path to neighbor is better, update the path
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristics[neighbor]
                open_list.put((f_score[neighbor], neighbor))

    return None  # Return None if no path is found

# Define the graph with nodes and weighted edges
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'D': 2, 'E': 5},
    'C': {'F': 1},
    'D': {'G': 3},
    'E': {'G': 2},
    'F': {'G': 2},
    'G': {}
}

# Define heuristic values for each node
heuristics = {
    'A': 7,
    'B': 6,
    'C': 2,
    'D': 3,
    'E': 1,
    'F': 1,
    'G': 0
}

# Set the start and goal nodes
start = 'A'
goal = 'G'

# Run the A* Search algorithm
path = a_star_search(graph, start, goal, heuristics)
print("Path found:", path)