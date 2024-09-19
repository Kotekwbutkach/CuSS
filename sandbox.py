import os

import pygame

from analyst import Analyst
from data.aliases import *
from models.ode_model_builder import OdeModelBuilder
from plotting import Plotter
from presentation import Presenter

NUMBER_OF_SIMULATIONS = 100
MODEL_ORDERS = [1, 2, 3, 4]
NUMBER_OF_DIMENSIONS = 2
NUMBER_OF_PARTICLES = 10
BOUNDS = ((0, 0), (600, 600))

COLORS = [
    pygame.Color("red"),
    pygame.Color("green"),
    pygame.Color("blue"),
    pygame.Color("orange")]

LABELS = ["model standardowy", "model rzędu 2", "model rzędu 3", "model rzędu 4"]

MODELS = [
    OdeModelBuilder()
    .with_default_phi_function(1, 2)
    .with_default_distance_function()
    .with_higher_order_cucker_smale_model(k)
    .build_for_time_step(0.05)
    for k in MODEL_ORDERS]

SIMULATION_PARAMETERS = [
    ((0, 5, 1, 1), 1000),
    ((0, 0, 1, 1), 1000),
    ((0, 25, 1, 1), 3000)]


def simulate_series(series_identifier: str, parameters: tuple[tuple[int, int, int, int], int]):
    print(f"Rozpoczęto Seria {series_identifier}")

    filepath = f".\\results\\Symulacja_{series_identifier}"
    number_of_steps = parameters[1]
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    all_trajectories_per_model = [list() for _ in MODEL_ORDERS]
    plotter = Plotter(filepath, LABELS)
    print(f"Ukończono 0/{NUMBER_OF_SIMULATIONS}.{len(MODEL_ORDERS)}", end='')
    for sim in range(NUMBER_OF_SIMULATIONS):
        initial_condition = np.zeros((2, NUMBER_OF_PARTICLES, 2))
        initial_condition[0, :, 0] = np.random.normal(parameters[0][0], parameters[0][1], NUMBER_OF_PARTICLES)
        initial_condition[0, :, 1] = np.random.normal(parameters[0][0], parameters[0][1], NUMBER_OF_PARTICLES)
        initial_condition[1, :, 0] = np.random.normal(parameters[0][2], parameters[0][3], NUMBER_OF_PARTICLES)
        initial_condition[1, :, 1] = np.random.normal(parameters[0][2], parameters[0][3], NUMBER_OF_PARTICLES)

        for i, model in enumerate(MODELS):
            traj = model.calculate_trajectory(initial_condition, number_of_steps)
            all_trajectories_per_model[i].append(traj)
            print(f"\rUkończono {sim + 1}.{i+1}/{NUMBER_OF_SIMULATIONS}.{len(MODEL_ORDERS)}", end='')

        # if sim == 0:
        #     colored_trajectories = list(zip([all_trajectories_per_model[i][0] for i in range(len(MODEL_ORDERS))], COLORS))
        #     presenter = Presenter(colored_trajectories)
        #     presenter.present()

    analysis_results = [Analyst.analyze(all_trajectories_per_model[i]) for i in range(len(MODEL_ORDERS))]
    colored_mean_results = list(zip((result for result in analysis_results), COLORS))
    plotter.plot_singles(colored_mean_results, f"Seria {series_identifier} - średnie parametry rozwiązań")
    print(f"\nUkończono Seria {series_identifier}")


if __name__ == "__main__":
    # simulate_series("1", SIMULATION_PARAMETERS[0])
    simulate_series("2", SIMULATION_PARAMETERS[1])
    # simulate_series("3", SIMULATION_PARAMETERS[2])
