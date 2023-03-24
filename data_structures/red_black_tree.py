RED = object()
BLACK = object()


class Node:
    def __init__(self, child, color):
        self.child = child
        self.color = color


class Root(Node):
    def __init__(self, child):
        super().__init__(child, BLACK)


class Tree:
    def __init__(self):
        self.root = Root(None)

        self.current_node = self.root

    def add_child(self, child: Node):
        if self.current_node.child is None:
            self.current_node.child = child
        else:
            raise ValueError
