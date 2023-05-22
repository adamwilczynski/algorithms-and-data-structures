from typing import Iterator
from collections import defaultdict, deque

import random


def generate_random_undirected_graph(vertex_count: int, edge_count: int) -> dict:
    # There is no node pointing to itself.

    if edge_count > vertex_count * (vertex_count - 1):
        raise ValueError("Wrong number of edges.")

    vertices = list(range(vertex_count))
    initial_vertices = random.choices(vertices, k=edge_count)

    possible_terminal_vertices = set(vertices)
    graph = defaultdict(list)
    for initial_vertex in zip(initial_vertices):
        terminal_vertex = (possible_terminal_vertices - {initial_vertex}).pop()
        graph[initial_vertex].append(terminal_vertex)
        graph[terminal_vertex].append(initial_vertex)
    return graph


def count_odd_degrees(graph):
    return sum(len(terminal_vertices) % 2 == 1 for terminal_vertices in graph.values())


def has_eulerian_trail(connected_graph):
    return count_odd_degrees(connected_graph) in (0, 2)

class DFS:
    def __init__(self):
        self.visited = set()

    def search(self, initial_vertex: int, graph: dict) -> deque:
        path = deque([initial_vertex])
        self.visited.add(initial_vertex)

        for neighbour in graph[initial_vertex]:
            if neighbour not in self.visited:
                path.extend(self.search(neighbour, graph))
        return path

def get_connected_graph_list(graph) -> [deque]:
    dfs = DFS()

    connected_graph_node_list = []
    for vertex in graph:
        if vertex not in dfs.visited:
            connected_graph_node_list.append(
                dfs(vertex)
            )
    return connected_graph_node_list

def hierholzer_euler_cycle(graph) -> Iterator[deque]:
    for connected_graph in get_connected_graph_list(graph):
        u = connected_graph.pop()
        stack = deque(u)
        result = deque()
        while stack:
            u = stack[-1]
            while graph[u]:
                v = graph[u].pop()
                stack.append(v)
                graph[v].remove(u)
                u = v
            result.append(stack.pop())
        yield result