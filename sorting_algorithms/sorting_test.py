import random

from abc import abstractmethod

from typing import MutableSequence


def get_fully_random_sequence(sequence_length: int, max_n: int):
    return [random.randint(1, max_n) for _ in range(sequence_length)]


def get_part_sorted_sequence(sequence_length: int, max_n: int):
    s = get_fully_random_sequence(sequence_length=sequence_length, max_n=max_n)
    number_of_sorts = random.randrange(sequence_length)
    start = 0
    for _ in range(number_of_sorts):
        end = random.randint(start, min(start + sequence_length // number_of_sorts, sequence_length))
        s = s[:start] + sorted(s[start:end]) + s[end:]
        start += sequence_length // number_of_sorts
    return s


def get_half_sorted_sequence(sequence_length: int, max_n: int):
    random_quarter = get_fully_random_sequence(sequence_length // 4, max_n)
    return random_quarter + sorted(random_quarter + random_quarter) + random_quarter


def get_fully_sorted_sequence(sequence_length: int, max_n: int):
    return sorted(get_fully_random_sequence(sequence_length=sequence_length, max_n=max_n))


class SortingAlgorithm:
    def __init__(self, sequence: MutableSequence | None):
        self.sequence = sequence

    @abstractmethod
    def sort(self) -> MutableSequence:
        seq = self.sequence
        pass

    @property
    @abstractmethod
    def is_stable(self) -> bool:
        pass


class BogoSort(SortingAlgorithm):
    def sort(self) -> MutableSequence:
        seq = self.sequence

        while self.sequence != sorted(self.sequence):
            random.shuffle(self.sequence)
        return self.sequence


class InsertionSort(SortingAlgorithm):
    def sort(self) -> MutableSequence:
        seq = self.sequence

        for i in range(1, len(seq)):
            for j in range(i, 0, -1):
                if seq[j - 1] > seq[j]:
                    seq[j - 1], seq[j] = seq[j], seq[j - 1]
                else:
                    break
        return seq


class SelectionSort(SortingAlgorithm):
    def sort(self) -> MutableSequence:
        seq = self.sequence

        for i in range(len(seq)):
            min_i = i
            for j in range(i + 1, len(seq)):
                if seq[j] < seq[min_i]:
                    min_i = j
            seq[i], seq[min_i] = seq[min_i], seq[i]
        return seq


class BubbleSort(SortingAlgorithm):
    def sort(self) -> MutableSequence:
        seq = self.sequence

        for i in range(len(seq)):
            for j in range(1, len(seq) - i):
                if seq[j - 1] > seq[j]:
                    seq[j - 1], seq[j] = seq[j], seq[j - 1]
        return self.sequence


class CountingSort(SortingAlgorithm):
    def sort(self) -> MutableSequence:
        seq = self.sequence


class QuickSort(SortingAlgorithm):

    def sort(self) -> MutableSequence:
        seq = self.sequence
        pass


class MergeSort(SortingAlgorithm):
    def sort(self) -> MutableSequence:
        seq = self.sequence

        if len(seq) > 1:
            mid_index = int(len(seq) / 2)

            left = seq[:mid_index]
            right = seq[mid_index:]
            # Sorting by recurrence
            self.__class__(left).sort()
            self.__class__(right).sort()

            # Merging
            left_index = 0
            right_index = 0
            sorted_index = 0

            while left_index < len(left) and right_index < len(right):
                # element from left is merged
                if left[left_index] <= right[right_index]:
                    seq[sorted_index] = left[left_index]
                    left_index += 1
                # element from right is merged
                else:
                    seq[sorted_index] = right[right_index]
                    right_index += 1
                sorted_index += 1

            while left_index < len(left):  # when all elements from right are merged
                seq[sorted_index] = left[left_index]
                left_index += 1
                sorted_index += 1

            while right_index < len(right):  # when all elements from left are merged
                seq[sorted_index] = right[right_index]
                right_index += 1
                sorted_index += 1

            return seq

    @property
    def is_stable(self) -> bool:
        return True


class HeapSort(SortingAlgorithm):
    def sort(self) -> MutableSequence:
        seq = self.sequence

        pass

    @property
    def is_stable(self) -> bool:
        return False


class ShellSort(SortingAlgorithm):
    pass


class TimSort(SortingAlgorithm):
    def sort(self) -> MutableSequence:
        seq = self.sequence

        return sorted(self.sequence)


class Sorting_Test:
    sorting_functions = [
        BubbleSort,
        InsertionSort,
        SelectionSort
    ]

    def __init__(self, test_sequence_length, test_max_n, tests_number):
        self.test_sequence_length = test_sequence_length
        self.test_max_n = test_max_n
        self.tests_number = tests_number

    def test(self):
        for _ in range(self.tests_number):
            random_sequence = get_fully_random_sequence(self.test_sequence_length, self.test_max_n)
            for sorting_algorithm in self.sorting_functions:
                function_sorted = sorting_algorithm(random_sequence.copy()).sort()
                assert function_sorted == sorted(random_sequence), (sorting_algorithm.__name__, function_sorted)


Sorting_Test(5, 25, 10).test()
