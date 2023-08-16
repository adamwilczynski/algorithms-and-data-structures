from sorting_algorithms import sorting_test
import common

sorting.Experiment(
    experiment_sequence_length_range=sorting.RANGE,
    max_n=sorting.MAX_N,
    experiment_number=common.EXPERIMENT_NUMBER,
    generate_input_function=sorting.get_half_sorted_sequence
).run_and_save_results_in_csv("half_sorted")
