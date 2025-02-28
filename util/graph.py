import seaborn as sns
import matplotlib.pyplot as plt

class Graph:
    def init(self, directed=False):
        self.directed = directed,
        self.nodes = set()
        self.adjacency_list = {}

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.add(node)
            self.adjacency_list[node] = {}

    def add_edge(self, node1, node2, weight=1):
        if node1 not in self.nodes:
            self.add_node(node1)
        if node2 not in self.nodes:
            self.add_node(node2)
        
        self.adjacency_list[node1][node2] = weight
        if not self.directed:
            self.adjacency_list[node2][node1] = weight

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            self.adjacency_list.pop(node, None)

            for neighbors in self.adjacency_list.values():
                neighbors.pop(node, None)
    
    def remove_edge(self, node1, node2):
        if node1 in self.adjacency_list:
            self.adjacency_list[node1].pop(node2, None)
        if not self.directed and node2 in self.adjacency_list:
            self.adjacency_list[node2].pop(node1, None)

    def plot(self):
        edges = []
        weights = []

        for start_node, neighbors in self.adjacency_list.items():
            for end_node, weight in neighbors.items():
                edges.append((start_node, end_node))
                weights.append(weight)
        
        plt.figure(figsize=(10,10))
        sns.heatmap(self._create_adjacency_matrix(), annot=True, cmap='Blues', cbar=True)
        plt.title('Graph')
        plt.xlabel('Nodes')
        plt.ylabel('Nodes')
        plt.show()

    def _create_adjacency_matrix(self):
        nodes = sorted(self.nodes)
        size = len(nodes)

        matrix = [[0] * size for _ in range(size)]
        node_indicies = {node: i for i,node in enumerate(nodes)}

        for start_node, neighbors in self.adjacency_list.items():
            for end_node, weight in neighbors.items():
                matrix[node_indicies[start_node][node_indicies[end_node]]] = weight
        
        return matrix

    def __repr__(self):
        return '\n'.join(f"{node}: {neighbors}" for node, neighbors in self.adjacency_list.items())
    
class Node:
    def __init__(self, data):
        data = data