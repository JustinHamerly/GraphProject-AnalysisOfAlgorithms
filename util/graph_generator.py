import random, itertools
from util.graph import Graph, Node

def generate_graph(
        min_nodes: int, max_nodes: int,
        min_edges: int, max_edges: int,
        data_string_list: list[str],
        directed: bool = False):
    
    g = Graph(directed)

    nodes = _generate_random_nodes(min_nodes, max_nodes, data_string_list)
    for n in nodes:
        g.add_node(n)
    
    num_edges = random.randint(min_edges, max_edges)
    valid_num = _is_valid_edge_count_range(len(nodes), num_edges, directed)
    if not valid_num:
        raise ValueError(f'Number of edges: {num_edges} is greater than the max number of valid edges for number of nodes: {len(nodes)}')
    
    list_nodes = list(nodes)
    random.shuffle(list_nodes)
    connected = {list_nodes[0]}
    remaining = set(list_nodes[1:])

    while remaining:
        node1 = random.choice(list(connected))
        node2 = random.choice(list(remaining))
        g.add_edge(node1, node2)
        connected.add(node2)
        remaining.remove(node2)

        if directed and num_edges > 1 and random.random() < .25:
            g.add_edge(node2, node1)
            num_edges -= 1
    
    remaining_edges = num_edges - (len(nodes) -1)
    if remaining_edges > 0:
        pairings = _get_random_pairings(nodes, remaining_edges, directed, g)
        for start, end in pairings:
            g.add_edge(start, end)

    return g



def _generate_random_nodes(min: int, max: int, data_options: list[str]):
    if min > len(data_options):
        raise ValueError('Range for min is greater than the number of items provided')
    if max > len(data_options):
        raise ValueError('Range for min is greater than the number of items provided')
    
    rand_number_nodes = random.randint(min, max)
    selected = random.sample(data_options, rand_number_nodes)
    nodes = set(Node(d) for d in selected)
    return nodes

def _is_valid_edge_count_range(node_count, edge_count, directed):
    max_edges = node_count * (node_count - 1)
    if not directed:
        max_edges = max_edges // 2
    return edge_count <= max_edges

def _get_random_pairings(nodes, num_pairings, directed, graph):
    if directed:
        possible_pairs = list(itertools.permutations(nodes, 2))
        new_pairings = [(a,b) for a,b in possible_pairs if b not in graph.adjacency_list[a]]
    else:
        possible_pairs = list(itertools.combinations(nodes,2))
        new_pairings = [(a,b) for a,b in possible_pairs if b not in graph.adjacency_list[a] and a not in graph.adjacency_list[b]]
    random_pairs = random.sample(new_pairings, min(num_pairings, len(possible_pairs)))
    return random_pairs