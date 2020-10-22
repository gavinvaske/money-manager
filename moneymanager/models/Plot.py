import matplotlib
import matplotlib.pyplot as plt
from os import path

class Plot:

    def __init__(self, x, y, xlabel, ylabel, title):
        self.x = x
        self.y = y

    def show(self):
        fig, ax = plt.subplots()
        ax.plot(self.x, self.y)
        ax.grid()
        plt.show()

    def save(self, file_name, directory=''):
        fig, ax = plt.subplots()
        ax.plot(self.x, self.y)
        ax.grid()
        file_path = path.join(directory, file_name + '.png')
        fig.savefig(file_path)


