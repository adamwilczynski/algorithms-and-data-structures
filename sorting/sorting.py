import random
import timeit
from abc import abstractmethod
from typing import MutableSequence


class SortingAlgorithm:
    def __init__(self, sequence: MutableSequence):
        self.sequence = sequence

    @abstractmethod
    def sort(self) -> MutableSequence:
        pass

    @property
    @abstractmethod
    def is_stable(self) -> bool:
        pass


class BogoSort(SortingAlgorithm):
    def sort(self) -> MutableSequence:
        while self.sequence != sorted(self.sequence):
            random.shuffle(self.sequence)
        return self.sequence


class InsertionSort(SortingAlgorithm):
    def sort(self) -> MutableSequence:
        for i in range(1, len(self.sequence)):
            j = i
            while j > 0 and self.sequence[j - 1] > self.sequence[j]:
                self.sequence[j - 1], self.sequence[j] = self.sequence[j], self.sequence[j - 1]
                j -= 1
        return self.sequence


class SelectionSort(SortingAlgorithm):
    def sort(self) -> MutableSequence:
        for i in range(len(self.sequence)):
            min_i = i
            for j in range(i + 1, len(self.sequence)):
                if self.sequence[j] < self.sequence[min_i]:
                    min_i = j
            self.sequence[i], self.sequence[min_i] = self.sequence[min_i], self.sequence[i]
        return self.sequence


class BubbleSort(SortingAlgorithm):
    pass


class CountingSort(SortingAlgorithm):
    pass


class QuickSort(SortingAlgorithm):
    pass


class MergeSort(SortingAlgorithm):
    def sort(self) -> MutableSequence:
        pass

    @property
    def is_stable(self) -> bool:
        return True


class HeapSort(SortingAlgorithm):
    def sort(self) -> MutableSequence:
        pass

    @property
    def is_stable(self) -> bool:
        return False


class ShellSort(SortingAlgorithm):
    pass


sorting_functions = [
    # BogoSort,
    InsertionSort,
    SelectionSort,
    BubbleSort,
    CountingSort
]


class RandomMutableSequenceGenerator:
    def __init__(self, sequence_length: int):
        self.random_sequence = list(range(sequence_length))

    def get_random_sequence(self):
        random.shuffle(self.random_sequence)
        return self.random_sequence


class Timer:
    pass


class Test:
    def __init__(self, test_sequence_length, tests_number):
        self.test_sequence_length = test_sequence_length
        self.tests_number = tests_number

    def test(self):
        random_sequence_generator = RandomMutableSequenceGenerator(self.test_sequence_length)
        for _ in range(self.tests_number):
            random_sequence = random_sequence_generator.get_random_sequence()
            for sorting_algorithm in sorting_functions:
                function_sorted = sorting_algorithm(random_sequence.copy()).sort()
                assert function_sorted == sorted(random_sequence), (sorting_algorithm.__name__, function_sorted)


# TODO: Report on 1 of the algorithms

Test(10, 10).test()

# Write on insertion and merge sort
# Arnold C bonus
