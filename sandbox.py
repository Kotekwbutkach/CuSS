import pygame

from data.aliases import *
from models.ode_model_builder import OdeModelBuilder
from plotting import Plotter
from presentation import Presenter

if __name__ == "__main__":
    NUMBER_OF_DIMENSIONS = 2
    NUMBER_OF_PARTICLES = 5
    NUMBER_OF_STEPS = 1000

    initial_condition = np.zeros((2, NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))
    initial_condition[0:] = (np.random.normal(10, 10, NUMBER_OF_DIMENSIONS * NUMBER_OF_PARTICLES)
                             .reshape(NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))
    initial_condition[1:] = (np.random.normal(5, 5, NUMBER_OF_DIMENSIONS * NUMBER_OF_PARTICLES)
                             .reshape(NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))

    BOUNDS = ((0, 0), (600, 600))

    def custom_phi(distances: np.ndarray):
        return np.ones(distances.shape)

    standard_model = (
        OdeModelBuilder()
        .with_default_phi_function(5, 2)
        .with_default_distance_function()
        .with_standard_cucker_smale_model()
        .build_for_time_step(0.05))

    higher_order_interactions_model = (
        OdeModelBuilder()
        .with_default_phi_function(5, 2)
        .with_default_distance_function()
        .with_higher_order_cucker_smale_model(2)
        .build_for_time_step(0.05))

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

    plotter = Plotter(trajectories, ".\\plots\\simulation_1")
    plotter.plot()
