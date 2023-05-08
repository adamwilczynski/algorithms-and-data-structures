from abc import ABC, abstractmethod
from collections import deque, namedtuple

input_graph = {
    1: [1, 2, 3],
    2: [3, 4],
    3: [1, 5],
    4: [2, 5],
    5: [2, 3]
}


class GraphSearchRecursiveAlgorithm(ABC):
    def __init__(self, graph, start, target):
        self.graph = graph
        self.start = start
        self.target = target

        self.visited = {self.start}

    @abstractmethod
    def search(self, way=None, current_node=None):
        pass


class DepthFirstSearch(GraphSearchRecursiveAlgorithm):
    def search(self, way=None, current_node=None):
        if way is None:
            way = [self.start]
            if self.start == self.target:
                return way
        if current_node is None:
            current_node = self.start

        for neighbour in self.graph[current_node]:
            if neighbour in self.visited:
                continue
            way.append(neighbour)
            print(f"visiting: {neighbour} way:{way}")
            self.visited.add(neighbour)
            if neighbour == self.target:
                return way

            if result_way := self.search(way=way, current_node=neighbour):
                return result_way
        return None


Node = namedtuple("Node", "value way")


class BreadthFirstSearch(GraphSearchRecursiveAlgorithm):
    def search(self, way=None, current_node=None):
        queue = deque([
            Node(self.start, [self.start])
        ])
        self.visited.add(self.start)

        while queue:
            current_node = queue.pop()
            if current_node.value == self.target:
                return current_node.way

            for neighbour_value in self.graph[current_node.value]:
                if neighbour_value not in self.visited:
                    queue.append(Node(neighbour_value, current_node.way + [neighbour_value]))
                    self.visited.add(neighbour_value)


print(DepthFirstSearch(input_graph, start=1, target=5).search())
print(BreadthFirstSearch(input_graph, start=1, target=4).search())
