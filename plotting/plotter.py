import os

import numpy as np
import pygame
from matplotlib import pyplot as plt


class Plotter:
    MAXIMUM_PREFIX = 'max_'
    DISTANCE_FILENAME = 'distance'

    filepath: str

    def __init__(
            self,
            trajectories: list[tuple[np.ndarray[float], pygame.Color]],
            filepath: str):
        self.trajectories = trajectories
        self.filepath = filepath

    def plot(self):
        fig = plt.figure()
        fig.suptitle("Zestawienie zależności od czasu parametrów analitycznych rozwiązań modeli")
        ax_x, ax_v = fig.subplots(1, 2)

        upper_bound_x, upper_bound_v = 0, 0

        for traj, color in self.trajectories:
            position = traj[0, :]
            velocity = traj[1, :]

            distance = np.tile(position, (5, 1, 1, 1)) - np.tile(position, (5, 1, 1, 1)).transpose(1, 0, 2, 3)
            max_of_distances = np.max(np.sqrt(np.sum(distance ** 2, axis=2)), axis=(0, 1))
            ax_x.plot(max_of_distances, color=tuple(c/255 for c in color))
            upper_bound_x = max(np.max(max_of_distances), upper_bound_x)

            max_of_velocities = np.max(np.sqrt(np.sum(velocity ** 2, axis=1)), axis=0)
            print(max_of_velocities.shape)
            ax_v.plot(max_of_velocities, color=tuple(c / 255 for c in color))
            upper_bound_v = max(np.max(max_of_velocities), upper_bound_v)

            print(max_of_distances)
            print(max_of_distances.shape)
            print(max_of_velocities)
            print(max_of_velocities.shape)
        ax_x.set_ylim((0, upper_bound_x * 1.1))
        ax_x.legend(["standardowy model", "model 3 rzędu"])
        ax_x.set_title("Maksymalna odległość pary cząstek")
        ax_v.set_ylim((0, upper_bound_v * 1.1))
        ax_v.legend(["standardowy model", "model 3 rzędu"])
        ax_v.set_title("Maksymalna prędkość cząstki")

        plt.show()
        plt.savefig(
            os.path.join(self.filepath, self.MAXIMUM_PREFIX + self.DISTANCE_FILENAME + '.png'),
            format='png')
