graph = {
    1: [2, 7],
    2: [3, 10],
    3: [4, 6],
    4: [5, 9],
    5: [6, 8],
    6: [1, 7],
    7: [8, 9],
    8: [2, 10],
    9: [11, 12],
    10: [5, 11],
    11: [3, 12],
    12: [1, 2]
}

graph_2 = {
    "A": "BFH",
    "B": "CI",
    "C:": "DFK",
    "D": "AE",
    "E": "FGL",
    "F": "EGH",
    "G": "CD",
    "H": "BCI",
    "I": "JK",
    "J": "HKL",
    "K": "EJ",
    "L": "AD"
}


def hamilton(graph, start_v):
    size = len(graph)
    # if None we are -unvisiting- comming back and pop v
    to_visit = [None, start_v]
    path = []
    while (to_visit):
        v = to_visit.pop()
        if v:
            path.append(v)
            if len(path) == size:
                break
            for x in set(graph[v]) - set(path):
                to_visit.append(None)  # out
                to_visit.append(x)  # in
        else:  # if None we are comming back and pop v
            path.pop()
    return path


for i in range(ord("A"), ord("A") + len(graph_2)):
    print(chr(i), hamilton(graph, chr(i)))
