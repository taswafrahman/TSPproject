import multiprocessing as mp
import time

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec

from .utility import rankify


# adapted from https://matplotlib.org/gallery/misc/multiprocess_sgskip.html
# by Robert Cimrman
class PlotHelper(object):
    """
    Plot helper class, assists with multithreading
    """

    def __init__(self, args):
        """
        Set up structures for plotting
        :param args: Our global parameter dictionary
        """
        self.args = args
        self.sender, receiver = mp.Pipe()
        self.plotter = RealPlotter()
        self.plot_process = mp.Process(
            target=self.plotter, args=(receiver,), daemon=True)
        self.plot_process.start()

    def plot(self, finished=False):
        """
        Moves data into the pipe, and signals the other process that something is waiting
        :param finished: Default to false, if changed to true,
        """
        send = self.sender.send
        if finished:
            send(None)
        else:
            data = (self.args['time'], self.args['max'],
                    self.args['mean'], self.args['sd'],
                    self.args['fitness'], self.args['population'],
                    self.args['dataset'], self.args['current_gen'],
                    self.args['generations'])
            send(data)


class RealPlotter(object):
    """
    This class plots data received from the multiprocessing pipe
    """

    def __init__(self):
        """ Dummy initializer, reserved for future use """
        pass

    def terminate(self):
        """ Signal to the plot to close """
        plt.close('all')

    def call_back(self):
        """ Callback to receive pipe data """

        # Poll the pipe
        while self.pipe.poll():
            # Look inside of the pipe and take the_box
            the_box = self.pipe.recv()

            # If the_box is empty, it's game over
            if the_box is None:
                self.terminate()
                return False

            # Otherwise, update the plot with the tools in the_box
            else:
                # Get our elapsed time
                elapsed_time = time.time() - the_box[0]

                # Add the elements to the plot
                self.ax1.plot(elapsed_time, the_box[1], c='tab:orange',
                              marker=r'$\clubsuit$', alpha=0.5,
                              markersize=10)
                self.ax1.plot(elapsed_time, the_box[2], c='tab:blue',
                              marker=r'$\clubsuit$',  alpha=0.5,
                              markersize=10)
                self.ax2.plot(elapsed_time, the_box[3], c='tab:pink',
                              marker=r'$\clubsuit$', alpha=0.5,
                              markersize=10)

                current_gen = the_box[-2]
                generations = the_box[-1]
                if current_gen == generations - 1:
                    x, y = self.get_path_coordinates(the_box[4], the_box[5], the_box[6])
                    self.ax3.plot(y, x, c='tab:olive', marker=r'$\clubsuit$',
                                  alpha=0.5, markersize=10)


        # Redraw the canvas
        self.fig.canvas.draw()
        return True

    def get_path_coordinates(self, fitness, population, dataset):
        x = rankify(fitness)

        x1, y = [], []
        for i in range(len(population[x[0]])):
            x1.append(dataset[population[x[0]][i]][0])
            y.append(-dataset[population[x[0]][i]][1])

        # Add the first city to connect to the last
        x1.append(dataset[population[x[0]][0]][0])
        y.append(-dataset[population[x[0]][0]][1])

        return [x1, y]

    def __call__(self, pipe):
        """ Support method for callback """
        self.pipe = pipe
        self.fig = plt.figure(tight_layout=True)
        self.gs = gridspec.GridSpec(2, 2)
        self.ax1 = self.fig.add_subplot(self.gs[0, 0])
        self.ax2 = self.fig.add_subplot(self.gs[1, 0])
        self.ax3 = self.fig.add_subplot(self.gs[:, 1])
        self.ax1.set_xlabel("Time")
        self.ax1.set_ylabel("Fitness")
        self.ax2.set_xlabel("Time")
        self.ax2.set_ylabel("Standard deviation")
        self.ax3.set_xlabel("Best path")
        orange_patch = mpatches.Patch(color='tab:orange', label='Best fitness')
        blue_patch = mpatches.Patch(color='tab:blue', label='Mean fitness')
        pink_patch = mpatches.Patch(color='tab:pink', label='Std. dev.')
        self.ax1.legend(handles=[orange_patch, blue_patch])
        self.ax2.legend(handles=[pink_patch])
        timer = self.fig.canvas.new_timer(interval=5)
        timer.add_callback(self.call_back)
        timer.start()
        plt.show()
