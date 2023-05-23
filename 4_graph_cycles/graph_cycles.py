import copy
from collections import deque

import random


def is_graph(graph: {int: [int]}):
    for initial_vertex in graph:
        for terminal_vertex in graph[initial_vertex]:
            if initial_vertex not in graph[terminal_vertex]:
                return False
    return True


def check_and_copy_graph(graph):
    if not is_graph(graph):
        raise ValueError("Not an undirected graph.")
    return copy.deepcopy(graph)


def generate_random_simple_graph(vertex_count: int, edge_count: int) -> dict:
    """O(v)"""
    if edge_count > vertex_count * (vertex_count - 1):
        raise ValueError("Wrong number of edges.")

    vertices = list(range(vertex_count))
    initial_vertices = random.choices(vertices, k=edge_count)

    all_vertices = set(vertices)

    graph = {v: [] for v in vertices}
    for initial_vertex in initial_vertices:
        possible_terminal_vertices = all_vertices - {initial_vertex} - set(graph[initial_vertex])
        if possible_terminal_vertices:
            terminal_vertex = possible_terminal_vertices.pop()
            graph[initial_vertex].append(terminal_vertex)
            graph[terminal_vertex].append(initial_vertex)
    return graph


def generate_euler_and_hamilton_cycle_graph(vertex_count: int):
    """O(v)"""
    vertices = list(range(vertex_count))
    return {
        initial_vertex: [vertices[initial_vertex - 1], initial_vertex + 1 if initial_vertex + 1 != vertex_count else 0]
        for initial_vertex in vertices
    }


def count_odd_degrees(graph: {int: [int]}):
    """O(v)"""
    return sum(len(terminal_vertices) % 2 == 1 for terminal_vertices in graph.values())


def has_euler_trail(connected_graph: {int: [int]}):
    """O(v)"""
    return count_odd_degrees(connected_graph) <= 2


class DFS:
    def __init__(self):
        self.visited = set()

    def traverse(self, initial_vertex: int, graph: {int: [int]}) -> deque:
        """O(v)"""
        path = deque([initial_vertex])
        self.visited.add(initial_vertex)

        for neighbour in graph[initial_vertex]:
            if neighbour not in self.visited:
                path.extend(self.traverse(neighbour, graph))
        return path


def get_connected_graph(graph: {int: [int]}, connected_graph_node_list: deque):
    """O(v)"""
    return {key: value for key, value in graph.items() if key in connected_graph_node_list}


def get_connected_graph_list(graph: {int: [int]}) -> [deque]:
    """O(v^2)"""
    dfs = DFS()

    connected_graph_node_list = []
    for vertex in graph:
        if vertex not in dfs.visited:
            connected_graph_node_list.append(
                get_connected_graph(graph, dfs.traverse(vertex, graph))
            )
    return connected_graph_node_list


def find_euler_cycle_using_hierholzer(connected_graph) -> deque:
    """O(v^2)"""
    connected_graph = check_and_copy_graph(connected_graph)

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


def find_hamiltonian_cycle_using_backtracking(connected_graph: {int: [int]}, path: [int]) -> [int]:
    """O(v!)"""
    connected_graph = check_and_copy_graph(connected_graph)

    if not path:
        path = list(connected_graph.keys())[:1]

    u = path[-1]

    if len(path) == len(connected_graph.keys()):
        v = path[0]
        if v in connected_graph[u]:
            return path
        return []

    for v in connected_graph[u]:
        if v not in path:
            if return_value := find_hamiltonian_cycle_using_backtracking(connected_graph, path + [v]):
                return return_value
    return []
