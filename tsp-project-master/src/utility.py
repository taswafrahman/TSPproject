import json
import os
import sys
import time

import argparse

import numpy as np


def order_subset_from_full_set(subset, full_set):
    """
    Arranges a subset in an order defined by another set

    :param subset: A list containing the elements we wish to order
    :param full_set: A superset of subset, from which we wish to extract order information
    :return: subset, with the order from full_set
    """
    new_order = subset[:]

    j = 0
    for i in range(len(full_set)):
        if full_set[i] in subset:
            new_order[j] = full_set[i]
            j += 1

    return new_order


def load_params_from_file(filename):
    """
    This function gets the required arguments for the EA from a JSON
    file and returns it as a dictionary.

    :return: EA args as a dictionary.
    """

    if not os.path.isfile(filename):
        die("File {filename} does not exist.".format(filename=filename))

    with open(filename, 'r') as f:
        args = json.load(f)

    return args


def parse_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--args-file', '-a',
                        default='default_args.json',
                        metavar='JSON_ARGUMENTS_FILE',
                        help='The JSON file that contains the arguments for the EA.')

    parser.add_argument('--test-runs', '-t',
                        type=int, default=1,
                        metavar='N',
                        help=('Number of times to run the algorithm. Used in conjunction '
                              'with --export-data'))

    parser.add_argument('--export', '-e',
                        action='store_true',
                        default=False,
                        help='Whether to export data to a CSV file or not.')

    parser.add_argument('--visualize', '-v',
                        action='store_true',
                        default=False,
                        help='Whether to visualize the data in real-time')

    parser.add_argument('--debug', '-d',
                        action='store_true',
                        default=False,
                        help='Turn on performance analytics and debugging output.')

    return parser.parse_args()


def print_performance_metrics(args):
    """
    Prints performance metrics for various parts of the EA.

    :param args: A dictionary with the EA parameters, what check_args() returns.
    """
    with CodeTimer('read datafile'):
        from src import data_import
        data_import.parse_datafile(args)

    with CodeTimer('calculate distance matrix'):
        data_import.calc_distance_matrix(args)

    with CodeTimer('generate starter population'):
        from src import initialize
        initialize.gen_population(args)

    with CodeTimer('initial eval time'):
        from src import evaluate
        evaluate.eval_population(args)

    with CodeTimer('parent selection'):
        from src import select
        select.parents(args)

    with CodeTimer('recombination'):
        from src import offspring_generation
        offspring_generation.recombination(args)

    with CodeTimer('mutation'):
        offspring_generation.mutation(args)

    with CodeTimer('offspring_fitness'):
        evaluate.eval_offspring(args)

    with CodeTimer('survivor selection'):
        select.survivors(args)
    print("Done evaluating performance")
    raise SystemExit


def print_config(args):
    """
    Output the relevant config parameters of the EA.

    :param args: The global parameter dictionary, as returned by check_args().
    :return:
    """

    print("\nRuntime parameters:")
    for k, v in sorted(args.items()):
        if k == "dataset" or k == "distance_matrix":
            continue
        print("\t'%s': %s" % (str(k), str(v)))
    print()


def rankify(values):
    """
    Rank an array

    :param values: An array of values
    :return: A ranking for the array of values
    """
    return np.argsort(np.array(values))[::-1]


def die(error):
    """
    Helper function to die on error

    :param error: Error message to display to user
    :return: Kills the program
    """

    print("Error: " + error)
    print("Usage: python3.5 " + str(sys.argv[0]) +
          " args-file-json (optional)")
    raise SystemExit

# CodeTimer derived from
# https://stackoverflow.com/questions/14452145/how-to-measure-time-taken-between-lines-of-code-in-python
# used to time each block, for profiling purposes
class CodeTimer:
    def __init__(self, name=None):
        self.name = "'" + name + "'" if name else ''

    def __enter__(self):
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_value, traceback):
        self.took = (time.perf_counter() - self.start) * 1000.0
        print("%s: %.2f ms" % (self.name, self.took))
