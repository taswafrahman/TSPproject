#!/usr/bin/env python3

import csv

from src import initialize, evaluate, offspring_generation, \
    select, data_import
from src.utility import *
import multiprocessing as mp
import matplotlib.pyplot as plt


def main():
    # Print header
    print("EA-TSP by E Garg, S Parson, T Rahman, J Wagner")

    # Get the command line arguments, and load the algorithm parameters
    # from a file. Also, read the data file and calculate the node distance
    # matrix.
    cmd_args = parse_args()
    args = load_params_from_file(cmd_args.args_file)
    data_import.parse_datafile(args)
    data_import.calc_distance_matrix(args)

    # Display the runtime arguments to the user
    print_config(args)

    ##########################################################################
    # COMMAND LINE ARG HANDLING
    ##########################################################################

    # Incompatible command line args
    if cmd_args.visualize and cmd_args.test_runs > 1:
        print("WARNING: Can't plot real-time data for more than one test run!")
        cmd_args.visualize = False

    # Just display algorithmic speed information for one generation and then
    # exit
    if cmd_args.debug:
        print_performance_metrics(args)

    # Create a graphical display if specified.
    if cmd_args.visualize:
        initialize.create_plotter(args)

    # If the user would like to export the results to a file, set up a
    # file to do so.
    export_fp = "{}.csv".format(cmd_args.args_file)
    if cmd_args.export:
        with open(export_fp, 'w') as fp:
            writer = csv.writer(fp, delimiter=',')
            writer.writerow(['run', 'best fitness'])

    ##########################################################################
    # MAIN LOOP
    ##########################################################################
    # Run the algorithm for the specified number of runs
    for run_num in range(cmd_args.test_runs):

        # Reinitialize population and fitness on a per-run basis
        initialize.gen_population(args)
        evaluate.eval_population(args)

        # Run each run for the specified number of generations
        for i in range(args['generations']):
            args['current_gen'] = i
            print("Generation %d: " % i, end="")
            select.parents(args)
            offspring_generation.recombination(args)
            offspring_generation.mutation(args)
            evaluate.eval_offspring(args)
            select.survivors(args)
            evaluate.print_stats(args)

            # Plot the current generation
            if cmd_args.visualize:
                evaluate.plot(args)

        evaluate.print_final(args, export_fp, run_num, cmd_args.export)


if __name__ == "__main__":
    # If we're on MacOSX, praise Steve Jobs first
    if plt.get_backend() == "MacOSX":
        mp.set_start_method("forkserver")
    main()
