import numpy as np
import pygame

from models.ode_model_factory import OdeModelFactory
from presentation import Presenter

if __name__ == "__main__":
    NUMBER_OF_DIMENSIONS = 2
    NUMBER_OF_PARTICLES = 5
    NUMBER_OF_STEPS = 1000


    def phi(s: float):
        return 1/(1+s**2)

    vector_phi = np.vectorize(phi)
    initial_condition = np.zeros((2, NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))
    initial_condition[0:] = (np.random.normal(300, 50, NUMBER_OF_DIMENSIONS * NUMBER_OF_PARTICLES)
                             .reshape(NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))
    initial_condition[1:] = (np.random.normal(5, 5, NUMBER_OF_DIMENSIONS * NUMBER_OF_PARTICLES)
                             .reshape(NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))

    state_checker = np.array([[[100*i + 10*j + k for k in range(2)] for j in range(7)] for i in range(2)])

    standard_model = OdeModelFactory.create_standard(0.05, vector_phi)
    higher_order_interactions_model = OdeModelFactory.create_higher_order(0.05, 3, vector_phi)

    standard_traj = standard_model.calculate_trajectory(
        initial_condition,
        NUMBER_OF_STEPS)
    higher_order_interactions_traj = higher_order_interactions_model.calculate_trajectory(
        initial_condition,
        NUMBER_OF_STEPS)

    trajectories = [
        (standard_traj, pygame.Color("green")),
        (higher_order_interactions_traj, pygame.Color("purple"))]

    presenter = Presenter(trajectories)
    presenter.present()

    presenter.get_boundaries()


