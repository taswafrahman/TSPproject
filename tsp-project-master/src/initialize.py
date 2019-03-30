import multiprocessing as mp
import time

import numpy as np

from src.plotter import PlotHelper


def gen_population(args):
    """
    Generate the initial population.

    :param args: The global parameter dictionary.
    """

    chromosome_length = len(args['dataset'])
    pop_size = args['pop_size']
    initialize_method = args['initialize_method']
    pop = []

    # Initialize the starting population as a randomly sampled set of the
    # permutation space.
    if initialize_method == 'random':
        for i in range(pop_size):
            pop.append(list(np.random.permutation(range(chromosome_length))))

    # Initialize the starting population as a randomly sampled set of the
    # permutation space, in a sequence of concatenated clusters using
    # the k-means algorithm.
    if initialize_method == 'kmeans':

        # Use multiple CPUs in a multiprocessing pool to do the
        # k-means algorithm in parallel
        number_of_cpus = mp.cpu_count()//2
        pool = mp.Pool(number_of_cpus)

        # Remove the plotter (because of MP)
        plotter = args.get("plotter")
        args.pop("plotter", None)

        # Collect a list of result objects for each of the individuals that
        # we would like to generate
        results = [pool.apply_async(kmeans, args=(args,)) for x in range(pop_size)]

        # Create the population by iterating over the result objects
        pop = [p.get() for p in results]

        # Wait for the processes to finish before exiting this function
        pool.close()
        pool.join()

        # Put the plotter back in
        args['plotter'] = plotter

    # Assign the new population to the dictionary
    args['population'] = pop


def kmeans(args):
    """
    Initialize the population using the k-means algorithm.

    :param args: The global parameter dictionary.
    """
    chromosome_length = len(args['dataset'])
    distance_matrix = args['distance_matrix']

    # Because of multiprocessing, reseed the RNG
    np.random.seed()

    # Get the number of clusters
    kca_k = args['kca_k']
    # kca_k is a proportion of the chromosome length
    kca_k = int(kca_k * chromosome_length)

    # Calculate cluster centers
    kca_cluster_centers = np.random.choice(range(chromosome_length), kca_k, replace=False)

    # Initialize an empty array of cities that correspond
    # to the centers
    kca_cluster_cities = [[] for x in range(kca_k)]

    # Assign every city to a particular cluster
    for city in range(chromosome_length):
        # Calculate the distance between a given city and every cluster
        # center
        distances = [distance_matrix[x][city] for x in kca_cluster_centers]
        # Pick the cluster that is closest to the given city
        min_d = np.argmin(distances)
        # Then, add the city to that closest cluster
        kca_cluster_cities[min_d].append(city)

    iteration = 0

    # kca_iterations defines for how many iterations the cluster centers
    # are refined. Usually, one would use a convergence a model to find an
    # appropriate stopping condition, but that turned out to be too
    # computationally expensive in our case.
    while iteration < args['kca_iterations']:
        iteration += 1

        # For every cluster
        for cluster_idx in range(len(kca_cluster_cities)):
            # If the cluster is empty, skip it
            if len(kca_cluster_cities[cluster_idx]) == 0:
                continue

            distances = []
            distance = 0

            # Find a new center for the given cluster if a better one exists
            # For every city city1 in the cluster, we add all the distances between
            # city1 and every other city and append it to the 'distances' list.
            for city_idx in range(len(kca_cluster_cities[cluster_idx])):
                for city_idx2 in range(len(kca_cluster_cities[cluster_idx])):
                    if city_idx == city_idx2:
                        continue
                    city1 = kca_cluster_cities[cluster_idx][city_idx]
                    city2 = kca_cluster_cities[cluster_idx][city_idx2]
                    distance += distance_matrix[city1][city2]
                distances.append(distance)

            # Pick the city with the smallest cumulative distance
            # every other city and make it the new center of the current
            # cluster.
            low_idx = np.argmin(distances)
            low_city = kca_cluster_cities[cluster_idx][low_idx]
            kca_cluster_centers[cluster_idx] = low_city

        # Order all the clusters by their centers, so that the closest
        # clusters stay close to each other.
        new_cluster = [kca_cluster_centers[0]]

        while len(new_cluster) < len(kca_cluster_centers):
            cluster_centers = []
            cluster_center_distances = []

            # For the right-most element of the new_cluster list
            # let's call it 'nc', calculate the distance
            # between nc and every other cluster center.
            for i in kca_cluster_centers:
                if i in new_cluster:
                    continue

                cluster_centers.append(i)
                cluster_center_distances.append(distance_matrix[i][new_cluster[-1]])

            # Pick the cluster that is closest to nc.
            smallest_cluster_idx = np.argmin(cluster_center_distances)
            # And append it to new_clusters.
            new_cluster.append(cluster_centers[smallest_cluster_idx])

        kca_cluster_centers = new_cluster

        # We need to re-assign cities to particular clusters again,
        # now that we've moved the centers around
        kca_cluster_cities = [[] for x in range(kca_k)]

        for city in range(chromosome_length):
            distances = [distance_matrix[x][city] for x in kca_cluster_centers]
            min_d = np.argmin(distances)
            kca_cluster_cities[min_d].append(city)

    # Convert the clustered 2-D chromosome to a 1-D sequence
    flattened_array = [kca_cluster_cities[x][y] for x in range(len(kca_cluster_cities)) \
                       for y in range(len(kca_cluster_cities[x]))]

    return flattened_array


def create_plotter(args):
    """ Create plotter object for realtime plotting"""

    # Store the current time, and the plotter object in the global object
    args['plotter'] = PlotHelper(args)
    args['time'] = time.time()
