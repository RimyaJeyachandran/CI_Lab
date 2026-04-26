import heapq
from collections import deque

class Graph:
    def __init__(self):
        # Using a dictionary where key = node, value = list of (neighbor, cost)
        self.adj_list = {}

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = []
            print(f"Node '{node}' added.")
        else:
            print("Node already exists.")

    def add_edge(self, u, v, cost=0):
        if u in self.adj_list and v in self.adj_list:
            # Check if edge already exists to prevent duplicates
            if any(neigh == v for neigh, _ in self.adj_list[u]):
                print("Edge already exists.")
            else:
                self.adj_list[u].append((v, cost))
                self.adj_list[v].append((u, cost))
                print(f"Edge added: {u} <-> {v} (cost: {cost})")
        else:
            print("Error: Both nodes must exist first.")

    def display(self):
        print("\n--- Current Graph ---")
        for node, neighbors in self.adj_list.items():
            print(f"{node} : {neighbors}")

    def _print_status(self, it, fringe, explored):
        # fringe contains tuples, we just want to show the node names
        f_nodes = [item[0] if isinstance(item[0], str) else item[1] for item in fringe]
        print(f"{it:<5} | {str(f_nodes):<35} | {sorted(list(explored))}")

    def search(self, start, goal, mode="BFS", direction="LR"):
        """
        Generic search function to handle BFS and DFS variants.
        direction: 'LR' (Left-to-Right) or 'RL' (Right-to-Left)
        """
        if start not in self.adj_list:
            return print("Start node not found.")

        explored = set()
        # Fringe stores: (current_node, path_taken)
        fringe = deque([(start, [start])])
        iteration = 1

        print(f"\nRunning {mode} ({direction})...")
        print(f"{'Iter':<5} | {'Fringe':<35} | {'Explored'}")
        print("-" * 65)

        while fringe:
            self._print_status(iteration, fringe, explored)
            
            # BFS uses popleft (Queue), DFS uses pop (Stack)
            node, path = fringe.popleft() if mode == "BFS" else fringe.pop()

            if node == goal:
                print(f"\nGoal '{goal}' found! Path: {' -> '.join(path)}")
                return

            if node not in explored:
                explored.add(node)
                neighbors = self.adj_list[node]
                
                # Reverse for LR DFS or RL BFS to maintain correct order
                if (mode == "DFS" and direction == "LR") or (mode == "BFS" and direction == "RL"):
                    neighbors = reversed(neighbors)

                for neigh, _ in neighbors:
                    if neigh not in explored:
                        fringe.append((neigh, path + [neigh]))
            iteration += 1

    def ucs(self, start, goal):
        """ Uniform Cost Search using a Priority Queue """
        pq = [(0, start, [start])] # (total_cost, node, path)
        explored = {} # stores node: min_cost to handle re-visiting with lower cost
        iteration = 1

        print(f"\nRunning UCS...")
        print(f"{'Iter':<5} | {'Frontier (Cost, Node)':<35} | {'Explored'}")
        print("-" * 65)

        while pq:
            cost, node, path = heapq.heappop(pq)

            if node == goal:
                print(f"\nGoal '{goal}' reached! Cost: {cost}, Path: {' -> '.join(path)}")
                return

            if node not in explored or cost < explored[node]:
                explored[node] = cost
                for neigh, edge_cost in self.adj_list[node]:
                    new_cost = cost + edge_cost
                    heapq.heappush(pq, (new_cost, neigh, path + [neigh]))
            
            # Simple status print
            print(f"{iteration:<5} | {str([(c, n) for c, n, p in pq]):<35} | {list(explored.keys())}")
            iteration += 1

# Quick test setup based on your logs
g = Graph()
for n in "ABCDEFGHIJ": g.add_node(n)
g.add_edge('A', 'B', 4); g.add_edge('A', 'C', 2); g.add_edge('A', 'D', 5)
g.add_edge('B', 'E', 3); g.add_edge('E', 'I', 3); g.add_edge('I', 'J', 5)

g.ucs('A', 'I')