import csv

import matplotlib.pyplot as plt

from .utility import *


def eval_population(args):
    """
    Evaluates a population's fitness

    :param args: The global parameter dictionary
    :return: Adds 'fitness' to the dictionary
    """

    population = args['population']
    distance_matrix = args['distance_matrix']

    fitness = []

    # For every individual in the population
    for individual_idx in range(len(population)):

        individual_sum = 0

        # Point at the individual
        individual = population[individual_idx]

        # Look at every city pair
        for allele_idx in range(len(individual) - 1):
            city1 = individual[allele_idx]
            city2 = individual[allele_idx + 1]

            # Add their distance to the total
            individual_sum += distance_matrix[city1][city2]

        # Add the distance from the last node, back to the starting node
        individual_sum += distance_matrix[individual[0]][individual[-1]]

        # Add this individual's sum to the list of fitnesses, as a negative
        # value, so that we view this as a maximization problem
        fitness.append(-individual_sum)

    args['fitness'] = fitness


def print_stats(args):
    """
    Print statistics about a current generation

    :param args:
    :param export:
    :param export_fp:
    :return:
    """
    fitness = args['fitness']
    args['max'] = -np.max(fitness)
    args['mean'] = -np.mean(fitness)
    args['sd'] = np.std(fitness)
    print("Max: %d\tMean: %d\tSD: %d" % (args['max'], args['mean'], args['sd']))

def plot(args):
    """
    Wrapper function to call the plotter.

    :param args: The global parameter dictionary
    :return:
    """
    args['plotter'].plot()


def print_final(args, export_fp, run_num, export=False):
    """
    Print the final fitness values

    :param args: The global parameter dictionary
    :param visualize: A boolean value, which indicates whether or not visualization is currently in use.
    :param export: A boolean value, which indicates whether or not the statistics are to be exported to a file.
    :return:
    """
    distribution = rankify(args['fitness'])
    print("The best individual: ")
    print("#%d (fitness: %d): %s" % (0, -args['fitness'][distribution[0]], args['population'][distribution[0]]))

    # Write the the output to a CSV file, if specified.
    if export:
        with open(export_fp, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([run_num, -args['fitness'][distribution[0]]])

    # We need to halt the program so that the user can examine the plots
    if args.get('plotter') is not None:
        try:
            input()
        except KeyboardInterrupt:
            print("\nExiting...")


def eval_offspring(args):
    population = args['offspring']
    distance_matrix = args['distance_matrix']

    fitness = []

    for individual_idx in range(len(population)):

        individual_sum = 0

        for allele_idx in range(len(population[individual_idx]) - 1):
            city1 = population[individual_idx][allele_idx]
            city2 = population[individual_idx][allele_idx + 1]
            individual_sum += distance_matrix[city1][city2]
        individual_sum += distance_matrix[population[individual_idx][0]][population[individual_idx][-1]]

        fitness.append(-individual_sum)

    args['offspring_fitness'] = fitness
