
import statistics

def load_data_from_file(filename):
    fitnesses = []
    with open(filename) as fp:
        lines = fp.readlines()[1:]
        for line in lines:
            run_num, fitness = line.split(',')
            fitness = fitness.strip()
            fitnesses.append(float(fitness))

    return fitnesses

if __name__ == '__main__':
    files = [
        'canada.json.csv', 'canada.json.times.csv',
        'western_sahara.json.csv', 'western_sahara.json.times.csv',
        'uruguay.json.csv', 'uruguay.json.times.csv'
    ]

    for filename in files:
        print("{}:".format(filename))
        values = load_data_from_file(filename)
        print("Average: {:.4f}".format(statistics.mean(values)))
        print("Best: {:.4f}".format(min(values)))
        print("-------------------------------------------------")
