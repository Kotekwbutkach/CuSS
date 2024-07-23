import numpy as np
import pygame

from data.aliases import *
from models.ode_model_factory import OdeModelFactory
from presentation import Presenter

if __name__ == "__main__":
    NUMBER_OF_DIMENSIONS = 2
    NUMBER_OF_PARTICLES = 5
    NUMBER_OF_STEPS = 5000


    def _phi(s: float):
        return 10/(1+s**2)

    def standard_distance(a1: np.ndarray, a2: np.ndarray):
        return np.sqrt(np.sum((a1 - a2) ** 2, axis=0))

    def modulo_distance_at(modulo_bounds: BoundaryInt):
        def modulo_distance(a1: np.ndarray, a2: np.ndarray):
            one_dim_modulo_mask = np.tile(modulo_bounds[1], (5, 5, 1)).transpose(2, 1, 0)
            modulo_adjustments = np.stack(
                [np.stack(
                    (one_dim_modulo_mask[0, :] * i,
                     one_dim_modulo_mask[1, :] * j)
                ) for i in range(-1, 2) for j in range(-1, 2)]
            )
            array_difference = np.tile(a1 - a2, (9, 1, 1, 1))
            distances = array_difference + modulo_adjustments
            return np.min(np.sqrt(np.sum(distances
                                         ** 2, axis=1)), axis=0)
        return modulo_distance

    phi = np.vectorize(_phi)
    initial_condition = np.zeros((2, NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))
    initial_condition[0:] = (np.random.normal(160, 20, NUMBER_OF_DIMENSIONS * NUMBER_OF_PARTICLES)
                             .reshape(NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))
    initial_condition[1:] = (np.random.normal(5, 5, NUMBER_OF_DIMENSIONS * NUMBER_OF_PARTICLES)
                             .reshape(NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))

    state_checker = np.array([[[100*i + 10*j + k for k in range(2)] for j in range(7)] for i in range(2)])

    BOUNDS = ((0, 0), (600, 600))

    standard_model = OdeModelFactory.create_standard(0.05, phi, modulo_distance_at(BOUNDS))
    higher_order_interactions_model = OdeModelFactory.create_higher_order(0.05, 2, phi)

    standard_traj = standard_model.calculate_trajectory(
        initial_condition,
        NUMBER_OF_STEPS,
        bounds=BOUNDS)
    higher_order_interactions_traj = higher_order_interactions_model.calculate_trajectory(
        initial_condition,
        NUMBER_OF_STEPS,
        bounds=BOUNDS)

    trajectories = [
        (standard_traj, pygame.Color("green")),
        (higher_order_interactions_traj, pygame.Color("purple"))]

    presenter = Presenter(trajectories, bounds=BOUNDS)
    presenter.present()

    presenter.get_boundaries()


