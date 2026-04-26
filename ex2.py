import heapq
from collections import defaultdict

class Graph:
    def __init__(self):
        # Using defaultdict removes the need for manual 'add_node' checks
        self.adj = defaultdict(list)

    def add_edge(self, u: str, v: str, cost: int):
        """Adds a directed edge. Nodes are created automatically."""
        # Humans prefer to skip duplicates silently or with a simple set check
        if not any(neighbor == v for neighbor, _ in self.adj[u]):
            self.adj[u].append((v, cost))

    def display(self):
        print("\n--- Adjacency List ---")
        for node, neighbors in self.adj.items():
            connections = ", ".join([f"{v}({c})" for v, c in neighbors])
            print(f"{node} -> {connections or 'No outgoing edges'}")

def get_heuristics(nodes, goal):
    """Prompts user for heuristic values."""
    h_table = {goal: 0}
    print(f"\n--- Enter Heuristics (Goal: {goal}) ---")
    for node in nodes:
        if node == goal: continue
        while True:
            try:
                h_table[node] = int(input(f"Estimated cost from {node} to {goal}: "))
                break
            except ValueError:
                print("Please enter a valid integer.")
    return h_table

def astar_search(graph, start, goal):
    if start not in graph.adj and goal not in graph.adj:
        print("Error: Start or goal node doesn't exist.")
        return

    h_table = get_heuristics(graph.adj.keys(), goal)
    
    # priority_queue: (f_score, g_score, current_node, path)
    pq = [(h_table[start], 0, start, [start])]
    visited = set() # Sets are much faster than lists for lookup

    print(f"\n{'Iter':<5} | {'Frontier (Node, f)':<30} | {'Visited'}")
    print("-" * 60)

    iteration = 1
    while pq:
        # Show state like a human debugger
        frontier_status = sorted([(n, f) for f, g, n, p in pq])
        print(f"{iteration:<5} | {str(frontier_status):<30} | {list(visited)}")

        f, g, current, path = heapq.heappop(pq)

        if current in visited:
            continue
        
        if current == goal:
            print(f"\nSuccess! Optimized Path: {' -> '.join(path)}")
            print(f"Total Path Cost: {g}")
            return

        visited.add(current)

        for neighbor, cost in graph.adj[current]:
            if neighbor not in visited:
                new_g = g + cost
                new_f = new_g + h_table.get(neighbor, 0)
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [neighbor]))
        
        iteration += 1

    print("Result: No path found.")

def build_graph():
    g = Graph()
    nodes = input("Enter nodes separated by space: ").split()
    # Pre-initialize nodes in defaultdict
    for n in nodes: _ = g.adj[n]

    print("Enter edges as 'u v cost' (or 'done' to finish):")
    while True:
        line = input("> ").strip().lower()
        if line == 'done': break
        try:
            u, v, cost = line.split()
            g.add_edge(u, v, int(cost))
        except ValueError:
            print("Invalid format. Try: A B 5")
    return g

def main():
    g = build_graph()
    
    actions = {
        '1': g.display,
        '2': lambda: astar_search(g, input("Start: "), input("Goal: ")),
        '3': build_graph,
        '4': exit
    }

    while True:
        print("\n[1] Display [2] A* Search [3] Reset [4] Exit")
        choice = input("Choice: ")
        
        if choice in actions:
            if choice == '3': g = actions[choice]() # Re-assign graph on reset
            else: actions[choice]()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()