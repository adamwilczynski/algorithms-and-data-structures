import csv
import datetime
import random
import time
import timeit

from abc import abstractmethod
from collections import namedtuple
from typing import MutableSequence

import numpy as np


def get_random_sequence(sequence_length: int, max_n: int):
    return np.random.randint(0, max_n, sequence_length)


class SortingAlgorithm:
    def __init__(self, sequence: np.array):
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
        if len(self.sequence) > 1:
            mid_index = int(len(self.sequence) / 2)

            left = self.sequence[:mid_index]
            right = self.sequence[mid_index:]
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
                    self.sequence[sorted_index] = left[left_index]
                    left_index += 1
                # element from right is merged
                else:
                    self.sequence[sorted_index] = right[right_index]
                    right_index += 1
                sorted_index += 1

            while left_index < len(left):  # when all elements from right are merged
                self.sequence[sorted_index] = left[left_index]
                left_index += 1
                sorted_index += 1

            while right_index < len(right):  # when all elements from left are merged
                self.sequence[sorted_index] = right[right_index]
                right_index += 1
                sorted_index += 1

            return self.sequence

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


class Test:
    sorting_functions = [
        # BogoSort,
        InsertionSort,
        SelectionSort,
        # BubbleSort,
        # CountingSort
    ]

    def __init__(self, test_sequence_length, test_max_n, tests_number):
        self.test_sequence_length = test_sequence_length
        self.test_max_n = test_max_n
        self.tests_number = tests_number

    def test(self):
        for _ in range(self.tests_number):
            random_sequence = get_random_sequence(self.test_sequence_length, self.test_max_n)
            for sorting_algorithm in self.sorting_functions:
                function_sorted = sorting_algorithm(random_sequence.copy()).sort()
                assert function_sorted == sorted(random_sequence), (sorting_algorithm.__name__, function_sorted)


class Timer:
    pass


ExperimentResults = namedtuple("ExperimentResults",
                               "sequence_length experiment_number selection_sort_time merge_sort_time tim_sort_time")


class Experiment:
    experiment_sequence_length_range = list(10 ** i for i in range(1, 5))
    max_n = 1_000
    experiment_number = 100

    sequence_length = None

    def selection_sort(self):
        return SelectionSort(get_random_sequence(self.sequence_length, self.max_n)).sort()

    def merge_sort(self):
        return MergeSort(get_random_sequence(self.sequence_length, self.max_n)).sort()

    def tim_sort(self):
        return sorted(get_random_sequence(self.sequence_length, self.max_n))

    def get_sorting_function_timer(self, sorting_function):
        return timeit.timeit(stmt=lambda: sorting_function(), number=self.experiment_number)

    def run_and_get_results(self) -> ExperimentResults:
        calculations = sum(length ** 2.35 for length in self.experiment_sequence_length_range) * self.experiment_number
        time_estimated = calculations / (10 ** 9)
        print(f"Time estimated: {round(time_estimated, 2)}s")
        start = time.time()

        for sequence_length in self.experiment_sequence_length_range:
            self.sequence_length = sequence_length
            yield ExperimentResults(
                sequence_length=sequence_length,
                experiment_number=self.experiment_number,
                selection_sort_time=self.get_sorting_function_timer(self.selection_sort),
                merge_sort_time=self.get_sorting_function_timer(self.merge_sort),
                tim_sort_time=self.get_sorting_function_timer(self.tim_sort),
            )
        print(f"Time measured: {time.time() - start}s")

    def run_and_save_results_in_csv(self):
        today = datetime.datetime.today()
        results = list(self.run_and_get_results())
        with open(f"results_{today.date()}-{today.hour}-{today.minute}", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(results[0]._fields)
            for row in results:
                w.writerow(row)


# Test(test_sequence_length=100, test_max_n=100, tests_number=100).test()
print(Experiment().run_and_save_results_in_csv())

# Write on insertion and merge sort
# Arnold C bonus
