import random
from collections import deque, namedtuple

import numpy as np

Edge = namedtuple("Edge", "v1 v2")


class DAG:
    def __init__(self, vertex_count: int, edge_count: int):
        self.vertex_count = vertex_count
        self.edge_count = edge_count

        self.edge_list_representation = self.create_random_directed_acyclic_graph()
        self.adjacency_list_representation = self._get_adjacency_list_representation()
        self.adjacency_matrix_representation = self._get_adjacency_matrix_representation()

        self.visited = None

    def get_all_possible_edges_acyclic(self):
        edge_list = []
        for i in range(1, self.vertex_count):
            for j in range(0, i):
                edge_list.append(Edge(j, i))
        return edge_list

    def create_random_directed_acyclic_graph(self) -> list:
        if self.edge_count > self.vertex_count * (self.vertex_count - 1):
            raise ValueError("Too many edges")
        edge_list = self.get_all_possible_edges_acyclic()
        random.shuffle(edge_list)
        return edge_list[:self.edge_count]

    def _get_adjacency_list_representation(self) -> dict:
        adjacency_list = {i: [] for i in range(self.vertex_count)}
        for v1, v2 in self.edge_list_representation:
            adjacency_list[v1].append(v2)
        return adjacency_list

    def _get_adjacency_matrix_representation(self) -> np.ndarray:
        adjacency_matrix = np.zeros((self.vertex_count, self.vertex_count), dtype=bool)
        for v1, v2 in self.edge_list_representation:
            adjacency_matrix[v1][v2] = True
        return adjacency_matrix

    def topological_sort_with_dfs_on_adjacency_list(self):
        stack = deque()
        self.visited = set()
        for vertex in self.adjacency_list_representation.keys():
            stack.extend(self._get_stack_from_dfs_on_adjacency_list(vertex))
        return list(stack)[::-1]

    def _get_stack_from_dfs_on_adjacency_list(self, vertex):
        stack = deque()
        if vertex not in self.visited:
            self.visited.add(vertex)
            for ascendant in self.adjacency_list_representation[vertex]:
                stack.extend(self._get_stack_from_dfs_on_adjacency_list(ascendant))
            stack.append(vertex)
        return stack

    def topological_sort_with_dfs_on_adjacency_matrix(self):
        stack = deque()
        self.visited = set()
        for vertex_index, vertex_ascendants in enumerate(self.adjacency_matrix_representation):
            stack.extend(self._get_stack_from_dfs_on_adjacency_matrix(vertex_index))
        return list(stack)[::-1]

    def _get_stack_from_dfs_on_adjacency_matrix(self, vertex_index):
        stack = deque()
        if vertex_index not in self.visited:
            self.visited.add(vertex_index)
            for ascendant_index, ascendant in enumerate(self.adjacency_matrix_representation[vertex_index]):
                if ascendant:
                    stack.extend(self._get_stack_from_dfs_on_adjacency_matrix(ascendant_index))
            stack.append(vertex_index)
        return stack

    @staticmethod
    def has_input_arc(vertex, edge_list: list[Edge]):
        return any(edge.v2 == vertex for edge in edge_list)

    def topological_sort_naive_on_edge_list(self):
        self.visited = set()
        edge_list = self.edge_list_representation

        result = []

        while edge_list:
            precedents_to_be_removed = set()
            for vertex in range(self.vertex_count):
                if vertex not in self.visited and not self.has_input_arc(vertex, edge_list):
                    self.visited.add(vertex)

                    result.append(vertex)
                    precedents_to_be_removed.add(vertex)
            edge_list = [edge for edge in edge_list if edge.v1 not in precedents_to_be_removed]
        result.extend(set(range(self.vertex_count)) - self.visited)
        return result
