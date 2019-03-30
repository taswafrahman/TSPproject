import math
import os.path
import pickle


def parse_datafile(args):
    """
    Parse the TSP data file

    :param args: The global parameter dictionary
    :return: Adds the 'dataset' to the dictionary
    """

    datafile = args['datafile']
    dataset = {}

    # Open the TSP data file
    with open(datafile, 'r') as inputfile:
        for line in inputfile:
            # Separate the elements by spaces
            elements = line.split()

            # Assign the x and y coordinates of the city to a tuple in the
            # data set. Note that while the data file is indexed at 1, we
            # would like to start at 0, so we have shifted the index.
            dataset[int(elements[0]) - 1] = (float(elements[1]), float(elements[2]))

    args['dataset'] = dataset


def calc_distance_matrix(args):
    """
    Calculate the distance matrix

    :param args: The global parameter dictionary
    :return: Adds the 'distance_matrix' to the dictionary
    """

    dataset = args['dataset']
    datafile = args['datafile']

    # Load the distance matrix from a file if it exists
    if os.path.isfile(datafile + ".distance"):
        with open(datafile + ".distance", "rb") as myfile:
            distance_matrix = pickle.load(myfile)

    # Otherwise, create the distance matrix and write it to a file
    # for easy parsing on subsequent runs.
    else:
        all_cities = range(len(dataset))
        distance_matrix = [[0 for city1 in all_cities] for city2 in all_cities]

        # Assign each value to the distance matrix
        for city1 in all_cities:
            for city2 in all_cities:
                distance_matrix[city1][city2] = math.sqrt((dataset[city1][0] - dataset[city2][0]) ** 2 + (
                        dataset[city1][1] - dataset[city2][1]) ** 2)

        # Write the distance matrix to a file
        f = open(datafile + ".distance", "wb")
        pickle.dump(distance_matrix, f)
        f.close()

    args['distance_matrix'] = distance_matrix
