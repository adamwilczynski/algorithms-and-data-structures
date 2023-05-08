import functools
from collections import namedtuple

import numpy as np

KnapsackItem = namedtuple("KnapsackItem", "value weight")

knapsack = [
    KnapsackItem(5, 7),
    KnapsackItem(10, 1),
    KnapsackItem(9, 9)
]


def solve_knapsack(input_knapsack, max_weight):
    matrix_height = 1 + len(input_knapsack)
    matrix_width = 1 + max_weight
    solution = np.zeros(shape=(matrix_height, matrix_width), dtype=int)

    for item_index in range(1, matrix_height):
        for allowed_weight in range(matrix_width):
            item = knapsack[item_index - 1]
            item_taken = False
            if item.weight <= allowed_weight and item.value > solution[item_index - 1][allowed_weight]:
                solution[item_index][allowed_weight] = item.value
                item_taken = True
            # max of previous
            solution[item_index][allowed_weight] += max(
                solution[i][allowed_weight - item_taken * item.weight]
                for i in range(item_index - 1, -1, -1)
            )
    return solution


print(solve_knapsack(knapsack, 10))


@functools.lru_cache
def get_number_of_possible_ways(destination, possible_steps: frozenset):
    if destination == 0:
        return 1

    number_of_possible_ways = 0
    for step in possible_steps:
        if destination - step >= 0:
            number_of_possible_ways += get_number_of_possible_ways(destination - step, possible_steps)
    return number_of_possible_ways


print(get_number_of_possible_ways(
    10,
    frozenset({1, 2, 5, 10, 20, 50, 100})
))
