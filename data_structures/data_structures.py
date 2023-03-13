class Node:
    pass


class EmptyNode(Node):
    def __init__(self):
        self.value = "EmptyNode"


class LinkedListNode(Node):
    def __init__(self, previous_node: Node, value, next_node: Node):
        self.previous_node = previous_node
        self.value = value
        self.next_node = next_node

    def __repr__(self):
        return f"LinkedListNode({self.value})"


class LinkedList:
    def __init__(self):
        self.current_node = EmptyNode
        self.head = self.current_node

    def append(self, value):
        if self.current_node is EmptyNode:
            self.current_node = LinkedListNode(self.current_node, value, EmptyNode())
            self.head = self.current_node
        else:
            self.current_node.next_node = LinkedListNode(self.current_node, value, EmptyNode())
            self.current_node = self.current_node.next_node

    def __iter__(self):
        print(isinstance(self.head, EmptyNode), self.head, self.head.previous_node)
        while (not isinstance(self.head, EmptyNode)) and (not isinstance(self.head.previous_node, EmptyNode)):
            self.head = self.head.previous_node
            print(self.head)
        return self

    def __next__(self):
        if isinstance(self.head, EmptyNode):
            raise StopIteration
        head = self.head
        self.head = self.head.next_node
        return head

    def __repr__(self):
        return f"[{', '.join(str(node.value) for node in self)}]"


test_linked_list = LinkedList()
test_linked_list.append(3)
print(test_linked_list)
test_linked_list.append(2)
test_linked_list.append(1)
print(test_linked_list)
