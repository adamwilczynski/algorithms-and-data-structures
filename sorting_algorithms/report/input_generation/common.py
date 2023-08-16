import csv
import datetime
import time
import timeit
from collections import namedtuple


EXPERIMENT_NUMBER = 1_00
RANGE = list(10 ** i for i in range(1, 5))
MAX_N = 1_000

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