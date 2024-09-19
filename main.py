import sys

import pygame
import tkinter as tk

from analyst import Analyst
from data.aliases import *
from models.ode_model_builder import OdeModelBuilder
from plotting import Plotter
from presentation import Presenter
from user_interface import BaseParamsFrame, NormalParamsFrame, ModelParamsFrame, PlotParamsFrame

if __name__ == "__main__":

    window = tk.Tk()
    should_start = False

    def start():
        global should_start
        should_start = True
        window.destroy()

    window.title("CoDyS - parameters")

    base_params_frame = BaseParamsFrame(window)
    model_params_frame = ModelParamsFrame(window)
    plot_params_frame = PlotParamsFrame(window)
    normal_params_frame = NormalParamsFrame(window)

    start_button = tk.Button(window, command=start, text="Start", font="Arial 12", pady=4)
    normal_distribution_param_string_vars = normal_params_frame.string_vars

    base_params_frame.grid(row=0, column=0, padx=10, pady=10)
    normal_params_frame.grid(row=1, column=0, padx=10, pady=10)
    model_params_frame.grid(row=2, column=0, padx=10, pady=10)
    plot_params_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="N")
    start_button.grid(row=2, column=1, padx=10, pady=10)

    var = tk.StringVar(value="5")

    window.mainloop()
    if not should_start:
        sys.exit()

    base_params = {var: int(base_params_frame.string_vars[var].get()) for var in base_params_frame.string_vars}
    normal_params = {var: float(normal_params_frame.string_vars[var].get()) for var in normal_params_frame.string_vars}
    model_params = {var: model_params_frame.string_vars[var].get() for var in model_params_frame.string_vars}
    plot_str_params = {var: plot_params_frame.string_vars[var].get() for var in plot_params_frame.string_vars}
    plot_bool_params = {var: plot_params_frame.boolean_vars[var].get() for var in plot_params_frame.boolean_vars}

    COLORS = [
        pygame.Color("red"),
        pygame.Color("green"),
        pygame.Color("blue"),
        pygame.Color("orange")]

    parsed_models_params = [(
            int(model_params[f"model {i+1}"])
            if model_params[f"model {i+1}"] != ''
            else None,
            COLORS[i])
        for i in range(4)]
    parsed_models_params = list(filter(lambda x: x[0] is not None, parsed_models_params))

    filepath = plot_str_params["folder filepath"]
    number_of_iterations = int(plot_str_params["iterations"])

    NUMBER_OF_DIMENSIONS = 2

    LABELS = [f"model rzędu {order}" for order, _ in parsed_models_params]

    models = [(
        OdeModelBuilder()
        .with_default_phi_function(1, 2)
        .with_default_distance_function()
        .with_higher_order_cucker_smale_model(k)
        .build_for_time_step(0.05),
        color)
        for k, color in parsed_models_params]

    initial_condition = np.zeros((2, base_params["particles"], 2))

    trajectories = [list() for _ in range(len(models))]

    for iteration in range(number_of_iterations):
        initial_condition[0, :, 0] = np.random.normal(
            normal_params["mean_x1"],
            normal_params["std_dev_x1"],
            base_params["particles"])
        initial_condition[0, :, 1] = np.random.normal(
            normal_params["mean_x2"],
            normal_params["std_dev_x2"],
            base_params["particles"])
        initial_condition[1, :, 0] = np.random.normal(
            normal_params["mean_v1"],
            normal_params["std_dev_v1"],
            base_params["particles"])
        initial_condition[1, :, 1] = np.random.normal(
            normal_params["mean_v2"],
            normal_params["std_dev_v2"],
            base_params["particles"])

        for i, (model, color) in enumerate(models):
            traj = model.calculate_trajectory(initial_condition, base_params["duration"])
            trajectories[i].append(traj)

        if iteration == 0:
            colored_trajectories = list(zip([trajectories[i][0] for i in range(len(models))], list(color for _, color in models)))
            presenter = Presenter(colored_trajectories)
            presenter.present()
            pygame.quit()

    plotter = Plotter(filepath, LABELS)
    analysis_results = [Analyst.analyze(traj_for_model) for traj_for_model in trajectories]
    colored_mean_results = list(zip((result for result in analysis_results), COLORS))

    plot_parameters = [(var, plot_bool_params[var], plot_str_params[f"{var} filename"]) for var in plot_bool_params]
    plotter.plot_singles(colored_mean_results, plot_parameters)

