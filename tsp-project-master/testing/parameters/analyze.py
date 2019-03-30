from scipy.stats import mannwhitneyu
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def load_data_from_file(filename):
    fitnesses = []
    with open(filename) as fp:
        lines = fp.readlines()[1:]
        for line in lines:
            run_num, fitness = line.split(',')
            fitness = fitness.strip()
            fitnesses.append(float(fitness))

    return fitnesses

def compute_mann_whitney_u(datafile1, datafile2):
    data1 = load_data_from_file(datafile1)
    data2 = load_data_from_file(datafile2)
    stat, p = mannwhitneyu(data1, data2, alternative='less')
    print('Statistics={:.3f}, p={:.4f}'.format(stat, p))

def create_box_plot_kca_k():
    data1 = load_data_from_file("kca_k_0_1.json.csv")
    data2 = load_data_from_file("kca_k_0_3.json.csv")
    data3 = load_data_from_file("kca_k_0_7.json.csv")
    all_data = [data1, data2, data3]
    labels = ['kca_k = 0.1', 'kca_k = 0.3', 'kca_k = 0.7']

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 4))

    bplot = axes.boxplot(all_data, vert=False, notch=True,
                         patch_artist=True, labels=labels)
    axes.set_title('kca_k and its influence on the initial population.')

    colors = ['tab:orange', 'tab:green', 'tab:red']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)

    axes.yaxis.grid(True)
    axes.set_ylabel('kca_k')
    axes.set_xlabel('Fitness (Euclidean distance)')

    plt.savefig("kca_k_boxplot.png", dpi=300)

def create_box_plot_box_n():
    data1 = load_data_from_file("best_order_cutting_points_50.json.csv")
    data2 = load_data_from_file("best_order_cutting_points_150.json.csv")
    data3 = load_data_from_file("best_order_cutting_points_250.json.csv")
    all_data = [data1, data2, data3]
    labels = ['n = 50', 'n = 150', 'n = 250']

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 4))

    bplot = axes.boxplot(all_data, vert=False, notch=True,
                         patch_artist=True, labels=labels)
    axes.set_title('No. of best order crossover points (n) and their influence')

    colors = ['tab:orange', 'tab:green', 'tab:red']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)

    axes.yaxis.grid(True)
    axes.set_ylabel('BOX crossover points (n)')
    axes.set_xlabel('Fitness (Euclidean distance)')

    plt.savefig("box_crossover_n_boxplot.png", dpi=300)

def create_box_plot_kca_iterations():
    data1 = load_data_from_file("kca_iterations_10.json.csv")
    data2 = load_data_from_file("kca_iterations_30.json.csv")
    data3 = load_data_from_file("kca_iterations_50.json.csv")
    data4 = load_data_from_file("kca_iterations_100.json.csv")
    all_data = [data1, data2, data3, data4]
    labels = ['i = 10', 'i = 30', 'i = 50', 'i = 100']

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 4))

    bplot = axes.boxplot(all_data, vert=False, notch=True,
                         patch_artist=True, labels=labels)
    axes.set_title('kca_iterations and its influence on the initial population')

    colors = ['tab:orange', 'tab:green', 'tab:red', 'tab:blue']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)

    axes.yaxis.grid(True)
    axes.set_ylabel('No. of iterations (i)')
    axes.set_xlabel('Fitness (Euclidean distance)')

    plt.savefig("kca_iterations_boxplot.png", dpi=300)

if __name__ == '__main__':
    print("Comparing kca_k = 0.3 to kca_k = 0.1:")
    compute_mann_whitney_u("kca_k_0_3.json.csv", "kca_k_0_1.json.csv")
    print("Comparing kca_k = 0.7 to kca_k = 0.3:")
    compute_mann_whitney_u("kca_k_0_7.json.csv", "kca_k_0_3.json.csv")
    print("-------------------------------------------------")

    print("Comparing kca_iterations = 30 to kca_iterations = 10:")
    compute_mann_whitney_u("kca_iterations_30.json.csv", "kca_iterations_10.json.csv")
    print("Comparing kca_iterations = 50 to kca_iterations = 30:")
    compute_mann_whitney_u("kca_iterations_50.json.csv", "kca_iterations_30.json.csv")
    print("Comparing kca_iterations = 100 to kca_iterations = 50:")
    compute_mann_whitney_u("kca_iterations_100.json.csv", "kca_iterations_50.json.csv")   
    print("-------------------------------------------------")

    print("Comparing box_cutting_points_n = 150 to box_cutting_points_n = 50:")
    compute_mann_whitney_u("best_order_cutting_points_150.json.csv",
                           "best_order_cutting_points_50.json.csv")
    print("Comparing box_cutting_points_n = 250 to box_cutting_points_n = 150:")
    compute_mann_whitney_u("best_order_cutting_points_250.json.csv",
                           "best_order_cutting_points_150.json.csv")
    print("-------------------------------------------------")

    create_box_plot_kca_k()
    create_box_plot_box_n()
    create_box_plot_kca_iterations()

