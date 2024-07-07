import os

import numpy as np

from data import ParticlesSystem
from matplotlib import pyplot as plt


class Plotter:
    POSITION_FILENAME = 'position'
    VELOCITY_FILENAME = 'velocity'
    ACCELERATION_FILENAME = 'acceleration'
    STD_DEV_FILENAME_PREFIX = 'stddev_'
    VALUES_FILENAME_PREFIX = 'values_'

    _filepath: str
    _time_range: range
    _data: np.ndarray
    _std_dev_data: np.ndarray

    def __init__(self, particles_system: ParticlesSystem, filepath: str):
        self._filepath = filepath
        self._time_range = range(particles_system.step_limit)
        data = particles_system.particle_data()
        sup_norm_data = np.array([
            data[:, 1:, 0:2].max(axis=2),
            data[:, 1:, 2:4].max(axis=2),
            data[:, 1:, 4:6].max(axis=2)])
        self._data = sup_norm_data
        self._std_dev_data = sup_norm_data.std(axis=1)

    def _prepare_dir(self):
        if not os.path.exists(self._filepath):
            os.makedirs(self._filepath)

    def plot_values(self):
        self._prepare_dir()
        plt.plot(self._time_range, self._data[0, :, :].transpose())
        plt.savefig(os.path.join(self._filepath, self.VALUES_FILENAME_PREFIX + self.POSITION_FILENAME + '.png'), format='png')
        plt.show()
        plt.plot(self._time_range, self._data[1, :, :].transpose())
        plt.savefig(os.path.join(self._filepath, self.VALUES_FILENAME_PREFIX + self.VELOCITY_FILENAME + '.png'), format='png')
        plt.show()
        plt.plot(self._time_range, self._data[2, :, :].transpose())
        plt.savefig(os.path.join(self._filepath, self.VALUES_FILENAME_PREFIX + self.ACCELERATION_FILENAME + '.png'), format='png')
        plt.show()

    def plot_std_dev(self):
        self._prepare_dir()
        plt.plot(self._time_range, self._std_dev_data[0, :].transpose())
        plt.savefig(
            os.path.join(self._filepath, self.STD_DEV_FILENAME_PREFIX + self.POSITION_FILENAME + '.png'),
            format='png')
        plt.show()
        plt.plot(self._time_range, self._std_dev_data[1, :].transpose())
        plt.savefig(
            os.path.join(self._filepath, self.STD_DEV_FILENAME_PREFIX + self.VELOCITY_FILENAME + '.png'),
            format='png')
        plt.show()
        plt.plot(self._time_range, self._std_dev_data[2, :].transpose())
        plt.savefig(
            os.path.join(self._filepath, self.STD_DEV_FILENAME_PREFIX + self.ACCELERATION_FILENAME + '.png'),
            format='png')
        plt.show()
