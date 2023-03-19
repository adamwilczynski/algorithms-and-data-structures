import csv
import datetime
import random
import time
import timeit

from abc import abstractmethod
from collections import namedtuple
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


class TimSort(SortingAlgorithm):
    def sort(self) -> MutableSequence:
        return sorted(self.sequence)


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
            random_sequence = get_fully_random_sequence(self.test_sequence_length, self.test_max_n)
            for sorting_algorithm in self.sorting_functions:
                function_sorted = sorting_algorithm(random_sequence.copy()).sort()
                assert function_sorted == sorted(random_sequence), (sorting_algorithm.__name__, function_sorted)


ExperimentResults = namedtuple("ExperimentResults",
                               "sequence_length experiment_number insertion_sort_time merge_sort_time tim_sort_time")


class Experiment:
    def __init__(self, experiment_sequence_length_range, max_n, experiment_number, generate_input_function):
        self.experiment_sequence_length_range = experiment_sequence_length_range
        self.max_n = max_n
        self.experiment_number = experiment_number
        self.generate_input_function = generate_input_function

        self.sequence_length = None

    def get_sorting_function_timer(self, sorting_algorithm: SortingAlgorithm):
        total_mean_time = 0
        for _ in range(self.experiment_number):
            sorting_algorithm.sequence = self.generate_input_function(
                sequence_length=self.sequence_length, max_n=self.max_n
            )
            total_mean_time += timeit.timeit(stmt=sorting_algorithm.sort, number=1) / self.experiment_number
        return total_mean_time

    def iterate_over_different_sequence_length_results(self) -> ExperimentResults:
        calculations = sum(length ** 2.5 for length in self.experiment_sequence_length_range) * self.experiment_number
        time_estimated = calculations / (10 ** 9)
        print(f"Time estimated: {round(time_estimated, 2)}s")
        start = time.time()

        insertion_sort = InsertionSort(sequence=None)
        merge_sort = MergeSort(sequence=None)
        tim_sort = TimSort(sequence=None)

        for sequence_length in self.experiment_sequence_length_range:
            self.sequence_length = sequence_length
            yield ExperimentResults(
                sequence_length=sequence_length,
                experiment_number=self.experiment_number,
                insertion_sort_time=self.get_sorting_function_timer(insertion_sort),
                merge_sort_time=self.get_sorting_function_timer(merge_sort),
                tim_sort_time=self.get_sorting_function_timer(tim_sort),
            )
        print(f"Time measured: {time.time() - start}s")

    def run_and_save_results_in_csv(self, file_name: str):
        today = datetime.datetime.today()
        results = self.iterate_over_different_sequence_length_results()
        with open(f"results_insertion_merge/{file_name}_{today.date()}-{today.hour}-{today.minute}.csv", "w",
                  newline="") as f:
            w = csv.writer(f)
            w.writerow(ExperimentResults._fields)
            for row in results:
                w.writerow(row)


# Test(test_sequence_length=100, test_max_n=100, tests_number=100).test()
RANGE = list(10 ** i for i in range(1, 5))
MAX_N = 1_000
EXPERIMENT_NUMBER = 1_00

# Write on insertion and merge sort
# Arnold C bonus

# Problem - random generation differs
