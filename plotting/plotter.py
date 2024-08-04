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
        (ax_mean_x, ax_mean_v), (ax_max_x, ax_max_v) = fig.subplots(2, 2)

        upper_bound_x, upper_bound_v = 0, 0

        for traj, color in self.trajectories:
            number_of_particles = traj.shape[1]

            position = traj[0, :]
            velocity = traj[1, :]

            position_distance = (
                np.tile(position, (number_of_particles, 1, 1, 1))
                - np.tile(position, (number_of_particles, 1, 1, 1)).transpose(1, 0, 2, 3))
            mean_of_position_distances = np.mean(np.sqrt(np.sum(position_distance ** 2, axis=2)), axis=(0, 1))
            ax_mean_x.plot(mean_of_position_distances, color=tuple(c/255 for c in color))
            upper_bound_x = max(np.max(mean_of_position_distances), upper_bound_x)

            velocity_distance = (
                np.tile(velocity, (number_of_particles, 1, 1, 1))
                - np.tile(velocity, (number_of_particles, 1, 1, 1)).transpose(1, 0, 2, 3))
            mean_of_velocity_distances = np.mean(np.sqrt(np.sum(velocity_distance ** 2, axis=2)), axis=(0, 1))
            ax_mean_v.plot(mean_of_velocity_distances, color=tuple(c / 255 for c in color))
            upper_bound_v = max(np.max(mean_of_velocity_distances), upper_bound_v)

            position_distance = (
                np.tile(position, (number_of_particles, 1, 1, 1))
                - np.tile(position, (number_of_particles, 1, 1, 1)).transpose(1, 0, 2, 3))
            max_of_position_distances = np.max(np.sqrt(np.sum(position_distance ** 2, axis=2)), axis=(0, 1))
            ax_max_x.plot(max_of_position_distances, color=tuple(c/255 for c in color))
            upper_bound_x = max(np.max(max_of_position_distances), upper_bound_x)

            velocity_distance = (
                np.tile(velocity, (number_of_particles, 1, 1, 1))
                - np.tile(velocity, (number_of_particles, 1, 1, 1)).transpose(1, 0, 2, 3))
            max_of_velocity_distances = np.max(np.sqrt(np.sum(velocity_distance ** 2, axis=2)), axis=(0, 1))
            ax_max_v.plot(max_of_velocity_distances, color=tuple(c / 255 for c in color))
            upper_bound_v = max(np.max(max_of_velocity_distances), upper_bound_v)

        ax_mean_x.set_ylim((0, upper_bound_x * 1.1))
        ax_mean_x.legend(["standardowy model", "model 3 rzędu"])
        ax_mean_x.set_title("Średnia odległość pary cząstek")
        ax_mean_v.set_ylim((0, upper_bound_v * 1.1))
        ax_mean_v.legend(["standardowy model", "model 3 rzędu"])
        ax_mean_v.set_title("Średnia różnica prędkości pary cząstek")
        ax_max_x.set_ylim((0, upper_bound_x * 1.1))
        ax_max_x.legend(["standardowy model", "model 3 rzędu"])
        ax_max_x.set_title("Maksymalna odległość pary cząstek")
        ax_max_v.set_ylim((0, upper_bound_v * 1.1))
        ax_max_v.legend(["standardowy model", "model 3 rzędu"])
        ax_max_v.set_title("Maksymalna różnica prędkości pary cząstek")

        plt.show()
        plt.savefig(
            os.path.join(self.filepath, self.MAXIMUM_PREFIX + self.DISTANCE_FILENAME + '.png'),
            format='png')
