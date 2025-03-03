from graphviz import Digraph, Graph as UndirectedGraph

class Graph:
    def __init__(self, directed=False):
        self.directed = directed
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
        graph = Digraph() if self.directed else UndirectedGraph(strict=True)
        if not self.directed:
            graph.attr('edge', dir='none')
        for node in self.nodes:
            graph.node(str(node))

        for node, neighbors in self.adjacency_list.items():
            for neighbor, weight in neighbors.items():
                graph.edge(str(node), str(neighbor), label=str(weight))
        
        graph.view()


    def __repr__(self):
        return '\n'.join(f"{node}: {neighbors}" for node, neighbors in self.adjacency_list.items())
    
class Node:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"Node({self.data})"

    def __eq__(self, other):
        return self.data == other.data
    
    def __hash__(self):
        return hash(self.data)
