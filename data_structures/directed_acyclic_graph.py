from collections import deque

graph = {
    'root': ['a'],
    'a': ['b', 'e'],
    'b': ['c', 'd'],
    'd': ['e']
}

stack = deque(["root"])
visited = [False] * len(graph)

def check_children(node):
    global graph, stack, visited

    if
