from collections import deque

import random


def generate_random_simple_graph(vertex_count: int, edge_count: int) -> dict:
    if edge_count > vertex_count * (vertex_count - 1):
        raise ValueError("Wrong number of edges.")

    vertices = list(range(vertex_count))
    initial_vertices = random.choices(vertices, k=edge_count)

    possible_terminal_vertices = set(vertices)

    graph = {v: [] for v in vertices}
    for initial_vertex in initial_vertices:
        terminal_vertex = (possible_terminal_vertices - {initial_vertex}).pop()
        graph[initial_vertex].append(terminal_vertex)
        graph[terminal_vertex].append(initial_vertex)
    return graph


def count_odd_degrees(graph: {int: [int]}):
    return sum(len(terminal_vertices) % 2 == 1 for terminal_vertices in graph.values())


def has_euler_trail(connected_graph: {int: [int]}):
    return count_odd_degrees(connected_graph) <= 2


class DFS:
    def __init__(self):
        self.visited = set()

    def search(self, initial_vertex: int, graph: {int: [int]}) -> deque:
        path = deque([initial_vertex])
        self.visited.add(initial_vertex)

        for neighbour in graph[initial_vertex]:
            if neighbour not in self.visited:
                path.extend(self.search(neighbour, graph))
        return path


def get_connected_graph(graph: {int: [int]}, connected_graph_node_list: deque):
    return {key: value for key, value in graph.items() if key in connected_graph_node_list}


def get_connected_graph_list(graph: {int: [int]}) -> [deque]:
    dfs = DFS()

    connected_graph_node_list = []
    for vertex in graph:
        if vertex not in dfs.visited:
            connected_graph_node_list.append(
                get_connected_graph(graph, dfs.search(vertex, graph))
            )
    return connected_graph_node_list


def find_euler_cycle_using_hierholzer(connected_graph) -> deque:
    if not has_euler_trail(connected_graph):
        return deque()

    u = list(connected_graph.keys())[-1]
    stack = deque([u])
    result = deque()
    while stack:
        u = stack[-1]
        while connected_graph[u]:
            v = connected_graph[u].pop()
            stack.append(v)
            connected_graph[v].remove(u)
            u = v
        result.append(stack.pop())

    if result[0] == result[-1] and len(result) > 1:
        return result
    return deque()


def find_hamiltonian_cycle_using_backtracking(connected_graph: {int: [int]}, path: [int]) -> deque:
    u = path[-1]
    if len(path) == u:
        v = path[0]
        if v in connected_graph[u]:
            return path
        return deque()
    for v in connected_graph[u]:
        if v not in path:
            path.append(v)
            if return_value := find_hamiltonian_cycle_using_backtracking(connected_graph, path):
                return return_value
    return deque()
