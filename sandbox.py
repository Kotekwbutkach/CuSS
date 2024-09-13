import os

import pygame

from analyst import Analyst
from data.aliases import *
from models.ode_model_builder import OdeModelBuilder
from plotting import Plotter

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
    .with_default_phi_function(1, 3)
    .with_default_distance_function()
    .with_higher_order_cucker_smale_model(k)
    .build_for_time_step(0.05)
    for k in MODEL_ORDERS]

SIMULATION_PARAMETERS = [
    ((0, 1, 1, 1), 1000),
    ((0, 0, 1, 1), 1000),
    ((0, 20, 1, 1), 2000)]

def simulate_series(series_identifier: str, parameters: tuple[tuple[int, int, int, int], int]):
    filepath = f".\\results\\Symulacja_{series_identifier}"
    number_of_steps = parameters[1]

    if not os.path.exists(filepath):
        os.makedirs(filepath)

    all_trajectories_per_model = [list() for _ in MODEL_ORDERS]

    plotter = Plotter(filepath, LABELS)

    for sim in range(NUMBER_OF_SIMULATIONS):
        initial_condition = np.zeros((2, NUMBER_OF_PARTICLES, 2))
        initial_condition[0, :, 0] = np.random.normal(parameters[0][0], parameters[0][1], NUMBER_OF_PARTICLES)
        initial_condition[0, :, 1] = np.random.normal(parameters[0][0], parameters[0][1], NUMBER_OF_PARTICLES)
        initial_condition[1, :, 0] = np.random.normal(parameters[0][2], parameters[0][3], NUMBER_OF_PARTICLES)
        initial_condition[1, :, 1] = np.random.normal(parameters[0][2], parameters[0][3], NUMBER_OF_PARTICLES)

        flat_condition = initial_condition.reshape(4, NUMBER_OF_PARTICLES)

        np.savetxt(os.path.join(filepath, f"Parametry początkowe {sim + 1}.csv"), flat_condition, delimiter=",")

        trajectories_per_model = [model.calculate_trajectory(
            initial_condition,
            number_of_steps) for model in MODELS]

        for i in range(len(MODEL_ORDERS)):
            all_trajectories_per_model[i].append(trajectories_per_model[i])
        if sim == 0:
            analysis_results = [Analyst.analyze_single(trajectories_per_model[i]) for i in range(len(MODEL_ORDERS))]
            colored_results = list(zip(analysis_results, COLORS))
            plotter.plot_singles(
                colored_results,
                f"Wybrane parametry rozwiązania (N = {NUMBER_OF_PARTICLES})")

            # colored_trajectories = list(zip([trajectories_per_model[i] for i in range(len(MODEL_ORDERS))], COLORS))
            # presenter = Presenter(colored_trajectories)
            # presenter.present()
        for k, traj in enumerate(trajectories_per_model):

            flat_traj = traj.reshape(4 * NUMBER_OF_PARTICLES, number_of_steps+1)
            np.savetxt(os.path.join(filepath, f"Powtórzenie {sim+1} (model rzędu {k+1}).csv"), flat_traj, delimiter=",")

        print(f"Ukończono {sim+1}/{NUMBER_OF_SIMULATIONS}")

    analysis_results = [Analyst.analyze(all_trajectories_per_model[i]) for i in range(len(MODEL_ORDERS))]
    colored_mean_results = list(zip((result[0][1] for result in analysis_results), COLORS))

    plotter.plot_singles(colored_mean_results, f"Średnie parametry rozwiązań (N = {NUMBER_OF_PARTICLES})")


if __name__ == "__main__":
    simulate_series("1", SIMULATION_PARAMETERS[0])
    simulate_series("2", SIMULATION_PARAMETERS[1])
    simulate_series("3", SIMULATION_PARAMETERS[2])