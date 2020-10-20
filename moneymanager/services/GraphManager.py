import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class GraphManager:

    @staticmethod
    def generate_line_graph(x, y):
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set(xlabel='time (s)', ylabel='voltage (mV)',
               title='About as simple as it gets, folks')
        ax.grid()
        fig.savefig("test.png")
        plt.show()

