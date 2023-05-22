from collections import deque

import pytest

import graph_cycles


class TestGraphGeneration:
    @staticmethod
    def test_wrong_edge_number():
        with pytest.raises(ValueError):
            graph_cycles.generate_random_simple_graph(2, 3)

    @staticmethod
    def test_small_graph_generation():
        node_count = 5
        edge_count = 2
        graph = graph_cycles.generate_random_simple_graph(node_count, edge_count)

        assert len(graph) == node_count and 2 * edge_count == sum(
            len(vertex_list) for vertex_list in graph.values()
        )


class TestConnectedGraphFunctions:
    connected_graph = {
        1: [2, 3],
        2: [1, 3],
        3: [1, 2],
    }

    def test_count_odd_degrees(self):
        assert graph_cycles.count_odd_degrees(self.connected_graph) == 0

    def test_has_euler_trail(self):
        assert graph_cycles.has_euler_trail(self.connected_graph)

    def test_dfs(self):
        dfs = graph_cycles.DFS()
        assert dfs.search(1, self.connected_graph) == deque([1, 2, 3])


class TestDisconnectedGraphFunctions:
    disconnected_graph = {
        1: [2, 3],
        2: [1, 3],
        3: [1, 2],

        4: [5, 6],
        5: [4],
        6: [4],

        7: [],
    }

    def test_count_odd_degrees(self):
        print(self.disconnected_graph)
        assert graph_cycles.count_odd_degrees(self.disconnected_graph) == 2

    def test_has_euler_trail(self):
        print(self.disconnected_graph)
        assert graph_cycles.has_euler_trail(self.disconnected_graph)

    def test_get_connected_graph_list(self):
        print(self.disconnected_graph)
        assert graph_cycles.get_connected_graph_list(self.disconnected_graph) == [
            {1: [2, 3], 2: [1, 3], 3: [1, 2]},
            {4: [5, 6], 5: [4], 6: [4]},
            {7: []},
        ]

    @classmethod
    def test_hierholzer_euler_cycle(self):
        print(self.disconnected_graph)
        assert [
                   graph_cycles.find_euler_cycle_using_hierholzer(connected_graph)
                   for connected_graph in graph_cycles.get_connected_graph_list(self.disconnected_graph)
               ] == [
                   deque([3, 1, 2, 3]),
                   deque([]),
                   deque([]),
               ]

    def test_hamiltonian_backtracking(self):
        print(self.disconnected_graph)
        assert [
            graph_cycles.find_hamiltonian_cycle_using_backtracking(connected_graph, [1])
            for connected_graph in graph_cycles.get_connected_graph_list(self.disconnected_graph)
        ] == [
            deque([1, 2, 3]),
            deque(),
            deque(),
        ]
