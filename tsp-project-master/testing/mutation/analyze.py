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
    data1 = load_data_from_file("cyclic.json.csv")
    data2 = load_data_from_file("inversion.json.csv")
    data3 = load_data_from_file("insertion.json.csv")
    data4 = load_data_from_file("permutation_swap.json.csv")
    data5 = load_data_from_file("two_opt.json.csv")
    data6 = load_data_from_file("scramble.json.csv")
    indices = list(range(1, 31))

    plt.figure(1, figsize=(10.0, 10.0), dpi=300)
    plt.xlabel("Runs (n=30)")
    plt.ylabel("Fitness (Euclidean distance)")
    plt.title("Cyclic mutation vs. others")

    plt.plot(indices, data1, c='tab:orange',
             marker=r'$\clubsuit$', alpha=0.5,
             markersize=12)
    plt.plot(indices, data2, c='tab:green',
             marker=r'$\clubsuit$', alpha=0.5,
             markersize=12)
    plt.plot(indices, data3, c='tab:blue',
             marker=r'$\clubsuit$', alpha=0.5,
             markersize=12)
    plt.plot(indices, data4, c='tab:red',
             marker=r'$\clubsuit$', alpha=0.5,
             markersize=12)
    plt.plot(indices, data5, c='tab:pink',
             marker=r'$\clubsuit$', alpha=0.5,
             markersize=12)
    plt.plot(indices, data6, c='tab:gray',
             marker=r'$\clubsuit$', alpha=0.5,
             markersize=12)

    orange_patch = mpatches.Patch(color='tab:orange', label='Cyclic', alpha=0.5)
    green_patch = mpatches.Patch(color='tab:green', label='Inversion', alpha=0.5)
    blue_patch = mpatches.Patch(color='tab:blue', label='Insertion', alpha=0.5)
    red_patch = mpatches.Patch(color='tab:red', label='Permutation swap', alpha=0.5)
    pink_patch = mpatches.Patch(color='tab:pink', label='Two-Opt', alpha=0.5)
    gray_patch = mpatches.Patch(color='tab:gray', label='Scramble', alpha=0.5)

    plt.legend(handles=[orange_patch, green_patch, blue_patch,
                        red_patch, pink_patch, gray_patch],
               bbox_to_anchor=(0.5, 1.125), loc='upper center',
               ncol=3)
    plt.savefig("line_plot.png", dpi=300)

def create_box_plot():
    data1 = load_data_from_file("cyclic.json.csv")
    data2 = load_data_from_file("inversion.json.csv")
    data3 = load_data_from_file("insertion.json.csv")
    data4 = load_data_from_file("permutation_swap.json.csv")
    data5 = load_data_from_file("two_opt.json.csv")
    data6 = load_data_from_file("scramble.json.csv")
    all_data = [data1, data2, data3, data4, data5, data6]
    labels = ['Cyclic', 'Inversion', 'Insertion', 'Permutation\nSwap',
              'Two-Opt', 'Scramble']

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 4))

    bplot = axes.boxplot(all_data, vert=False, notch=True,
                         patch_artist=True, labels=labels)
    axes.set_title('Cyclic mutation vs. others')

    colors = ['tab:orange', 'tab:green', 'tab:blue',
              'tab:red', 'tab:pink', 'tab:gray']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.5)

    axes.yaxis.grid(True)
    axes.set_ylabel('Mutation operators')
    axes.set_xlabel('Fitness (Euclidean distance)')

    plt.savefig("boxplot.png", dpi=300)

if __name__ == '__main__':
    files = {
        'Scramble operator': 'scramble.json.csv',
        'Insertion operator': 'insertion.json.csv',
        'Inversion operator': 'inversion.json.csv',
        'Permutation Swap operator': 'permutation_swap.json.csv',
        'Two-Opt operator': 'two_opt.json.csv',
    }

    for operator, filename in files.items():
        print("Comparing Cyclic operator to {}:".format(operator))
        compute_mann_whitney_u("cyclic.json.csv", filename)
        print("-------------------------------------------------")

    create_box_plot()
    create_line_plot()

