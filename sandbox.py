import numpy as np
import pygame

from data.aliases import *
from models.ode_model_builder import OdeModelBuilder
from presentation import Presenter

if __name__ == "__main__":
    NUMBER_OF_DIMENSIONS = 2
    NUMBER_OF_PARTICLES = 5
    NUMBER_OF_STEPS = 5000

    initial_condition = np.zeros((2, NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))
    initial_condition[0:] = (np.random.normal(160, 20, NUMBER_OF_DIMENSIONS * NUMBER_OF_PARTICLES)
                             .reshape(NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))
    initial_condition[1:] = (np.random.normal(5, 5, NUMBER_OF_DIMENSIONS * NUMBER_OF_PARTICLES)
                             .reshape(NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))

    state_checker = np.array([[[100*i + 10*j + k for k in range(2)] for j in range(7)] for i in range(2)])

    BOUNDS = ((0, 0), (600, 600))

    standard_model = (OdeModelBuilder()
                      .with_default_phi_function(10, 2)
                      .with_modulo_distance_function(BOUNDS)
                      .with_standard_cucker_smale_model()
                      .build_for_time_step(0.05))

    higher_order_interactions_model = (OdeModelBuilder()
                      .with_default_phi_function(10, 2)
                      .with_modulo_distance_function(BOUNDS)
                      .with_higher_order_cucker_smale_model(3)
                      .build_for_time_step(0.05))

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


