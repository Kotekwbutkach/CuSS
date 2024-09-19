import os

import numpy as np
import pygame
from matplotlib import pyplot as plt


class Plotter:
    MAXIMUM_PREFIX = 'max_'
    DISTANCE_FILENAME = 'distance'

    filepath: str
    labels: list[str]

    def __init__(
            self,
            filepath: str,
            labels: list[str]):
        self.filepath = filepath
        self.labels = labels

    def plot_singles(
            self,
            colored_results: list[tuple[list[list[np.ndarray]], pygame.Color]],
            title: str
    ):
        plot_labels = [
            x + " - " + y
            for x in ["Położenie", "Prędkość"]
            for y in ["minimalna odległość", "średnia odległość", "maksymalna odległość", "odchylenie standardowe"]]
        for i in range(8):
            fig, ax = plt.subplots()
            label = plot_labels[i]
            lower_bound = None
            upper_bound = None
            for colored_result in colored_results:
                measures, color = colored_result
                measure = [x for row in measures for x in row][i]

                ax.plot(measure, color=tuple(c / 255 for c in color))

                lower_bound = np.min(measure)/1.1 if lower_bound is None else min(lower_bound, np.min(measure))
                upper_bound = np.max(measure) if upper_bound is None else max(upper_bound, np.max(measure))
            margin = (upper_bound - lower_bound) * 0.05
            ax.set_ylim((lower_bound - margin, upper_bound + margin))
            # ax.set_title(label)
            ax.legend(self.labels)
            if not os.path.exists(self.filepath):
                os.makedirs(self.filepath)
            plt.savefig(
                os.path.join(self.filepath, f'{title} - {label}.png'),
                format='png')
            plt.close()
            # plt.show()
