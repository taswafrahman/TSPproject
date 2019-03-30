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

def create_line_plot():
    data1 = load_data_from_file("best_order.json.csv")
    data2 = load_data_from_file("cut_crossfill.json.csv")
    indices = list(range(1, 31))

    plt.figure(1, figsize=(10.0,6.0), dpi=300)
    plt.xlabel("Runs (n=30)")
    plt.ylabel("Fitness (Euclidean distance)")
    plt.title("Best order vs. cut and crossfill")

    plt.plot(indices, data1, c='tab:orange',
             marker=r'$\clubsuit$', alpha=0.5,
             markersize=12)
    plt.plot(indices, data2, c='tab:green',
             marker=r'$\clubsuit$', alpha=0.5,
             markersize=12)

    orange_patch = mpatches.Patch(color='tab:orange', label='Best Order')
    green_patch = mpatches.Patch(color='tab:green', label='Cut And Crossfill')
    plt.legend(handles=[orange_patch, green_patch])
    plt.savefig("best_order_vs_cut_crossfill.png", dpi=300)

def create_box_plot():
    data1 = load_data_from_file("best_order.json.csv")
    data2 = load_data_from_file("cut_crossfill.json.csv")
    all_data = [data1, data2]
    labels = ['Best order', 'Cut and crossfill']

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5, 4))

    bplot = axes.boxplot(all_data, vert=True, notch=True,
                         patch_artist=True, labels=labels)
    axes.set_title('Best order vs. cut and crossfill')

    colors = ['lightblue', 'lightgreen']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)

    axes.yaxis.grid(True)
    axes.set_xlabel('Crossover operators')
    axes.set_ylabel('Fitness (Euclidean distance)')

    plt.savefig("boxplot.png", dpi=300)

def create_histogram():
    data1 = load_data_from_file("best_order.json.csv")
    data2 = load_data_from_file("cut_crossfill.json.csv")

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    ax1.hist(data1, alpha=0.5,
             edgecolor='black', linewidth=1.2)
    ax1.set_xlabel('Fitness (Euclidean distance)')
    ax1.set_title('Best Order')

    ax2.hist(data2, alpha=0.5, label='Cut and Crossfill',
             edgecolor='black', linewidth=1.2, color='green')
    ax2.set_xlabel('Fitness (Euclidean distance)')
    ax2.set_title('Cut and Crossfill')

    plt.savefig("histogram.png", dpi=300)

if __name__ == '__main__':
    compute_mann_whitney_u("best_order.json.csv",
                           "cut_crossfill.json.csv")
    create_histogram()
    create_box_plot()
    create_line_plot()
