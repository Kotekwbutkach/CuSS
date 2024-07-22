from typing import Callable

import numpy as np

from data.aliases import *


class OdeModel:
    time_delta: float
    function: Callable[[np.ndarray], np.ndarray]

    def __init__(
            self,
            time_step: float,
            function: Callable[[np.ndarray], np.ndarray]):
        self.time_delta = time_step
        self.function = function

    def calculate_trajectory(
            self,
            initial_condition: np.ndarray,
            steps_limit: int,
            bounds: BoundaryInt | None) -> np.ndarray:
        trajectory = np.zeros(tuple([*initial_condition.shape, steps_limit + 1]))
        trajectory[:, :, :, 0] = initial_condition
        for t in range(steps_limit):
            trajectory[:, :, :, t + 1] = self.calculate_step(trajectory[:, :, :, t], bounds)
        return trajectory

    def calculate_step(
            self,
            state: np.ndarray,
            bounds: BoundaryInt | None) -> np.ndarray:
        k1 = self.function(state)
        k2 = self.function(state + (self.time_delta / 2) * k1)
        k3 = self.function(state + (self.time_delta / 2) * k2)
        k4 = self.function(state + self.time_delta * k3)
        delta = (k1 + (2 * k2) + (2 * k3) + k4)/6
        return self.correct_modulo(state + self.time_delta * delta, bounds)

    def correct_modulo(
            self,
            state: np.ndarray,
            bounds: BoundaryInt | None):
        positions = state[0]
        if bounds is None:
            return state
        below_bounds = np.tile(bounds[0], (5, 1))
        above_bounds = np.tile(bounds[1], (5, 1))
        positions = np.where(
            np.all((below_bounds <= positions, above_bounds >= positions), axis=0),
            positions,
            below_bounds + positions % (above_bounds - below_bounds))
        state[0] = positions
        return state
