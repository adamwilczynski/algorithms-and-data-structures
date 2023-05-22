import sorting

sorting.Experiment(
    experiment_sequence_length_range=sorting.RANGE,
    max_n=sorting.MAX_N,
    experiment_number=sorting.EXPERIMENT_NUMBER,
    generate_input_function=sorting.get_fully_random_sequence
).run_and_save_results_in_csv("fully_random")