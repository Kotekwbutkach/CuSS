import pygame

from data.aliases import *
from models.ode_model_builder import OdeModelBuilder
from plotting import Plotter
from presentation import Presenter

if __name__ == "__main__":
    NUMBER_OF_DIMENSIONS = 2
    NUMBER_OF_PARTICLES = 15
    NUMBER_OF_STEPS = 1000

    initial_condition = np.zeros((2, NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))
    initial_condition[0:] = (np.random.normal(10, 10, NUMBER_OF_DIMENSIONS * NUMBER_OF_PARTICLES)
                             .reshape(NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))
    initial_condition[1:] = (np.random.normal(5, 5, NUMBER_OF_DIMENSIONS * NUMBER_OF_PARTICLES)
                             .reshape(NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))

    BOUNDS = ((0, 0), (600, 600))

    def custom_phi(distances: np.ndarray):
        return np.ones(distances.shape)

    models = [
        OdeModelBuilder()
        .with_default_phi_function(1, 2)
        .with_default_distance_function()
        .with_higher_order_cucker_smale_model(k)
        .build_for_time_step(0.05)
        for k in range(1, 5)]

    trajectories = [model.calculate_trajectory(
        initial_condition,
        NUMBER_OF_STEPS) for model in models]

    colored_trajectories = list(zip(
        trajectories,
        [pygame.Color("red"),
         pygame.Color("green"),
         pygame.Color("blue"),
         pygame.Color("orange")]))

    presenter = Presenter(colored_trajectories)
    presenter.present()

    plotter = Plotter(colored_trajectories,
                      ["model standardowy", "model rzędu 2", "model rzędu 3", "model rzędu 4"],
                      ".\\plots\\simulation_1")
    plotter.plot()
