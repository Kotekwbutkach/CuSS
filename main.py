import sys
import tkinter as tk

import numpy as np
import pygame

from models.ode_model_builder import OdeModelBuilder
from user_interface.int_entry import IntEntry
from user_interface.normal_params_frame import NormalParamsFrame

if __name__ == "__main__":

    window = tk.Tk()
    should_start = False

    def start():
        global should_start
        should_start = True
        window.destroy()

    window.title("CoDyS - parameters")

    number_of_particles_str_var = tk.StringVar(value='5')

    number_of_particles_frame = tk.Frame(width=200, height=100)
    number_of_particles_entry = IntEntry(number_of_particles_frame, textvariable=number_of_particles_str_var, width=8)
    number_of_particles_label = tk.Label(number_of_particles_frame, text="Number of particles: ", font="Arial 9")

    number_of_particles_label.grid(row=0, column=0)
    number_of_particles_entry.grid(row=0, column=1)

    normal_params_frame = NormalParamsFrame(window)

    start_button = tk.Button(window, command=start, text="Start")
    normal_distribution_param_string_vars = normal_params_frame.string_vars

    number_of_particles_frame.grid(row=0, column=0)
    normal_params_frame.grid(row=1, column=0)
    start_button.grid(row=2, column=0)
    window.mainloop()

    print([[float(x.get()) for x in var] for var in normal_distribution_param_string_vars])

    if not should_start:
        sys.exit()

    NUMBER_OF_DIMENSIONS = 2
    NUMBER_OF_PARTICLES = 5
    NUMBER_OF_STEPS = 3000

    def phi(s: float):
        return 1/(1+s**2)

    vector_phi = np.vectorize(phi)
    initial_condition = np.zeros((2, NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))
    initial_condition[0:] = (np.random.normal(300, 50, NUMBER_OF_DIMENSIONS * NUMBER_OF_PARTICLES)
                             .reshape(NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))
    initial_condition[1:] = (np.random.normal(5, 5, NUMBER_OF_DIMENSIONS * NUMBER_OF_PARTICLES)
                             .reshape(NUMBER_OF_PARTICLES, NUMBER_OF_DIMENSIONS))

    state_checker = np.array([[[100*i + 10*j + k for k in range(2)] for j in range(7)] for i in range(2)])

    model1 = OdeModelBuilder.create_higher_order(0.05, 3, vector_phi)
    traj1 = model1.calculate_trajectory(initial_condition, NUMBER_OF_STEPS)

    model2 = OdeModelBuilder.create_standard(0.05, vector_phi)
    traj2 = model2.calculate_trajectory(initial_condition, NUMBER_OF_STEPS)

    pygame.init()
    pygame.display.set_mode((800, 800))
    surface = pygame.display.get_surface()
    pygame.display.set_caption('CoDyS')
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 20)

    STEP = 0

    surface.fill(pygame.Color("black"))

    def draw_particles():
        for i in range(traj1.shape[1]):
            pygame.draw.circle(
                surface,
                pygame.Color("purple"),
                (traj1[0, i, 0, STEP], traj1[0, i, 1, STEP]),
                5)

        for i in range(traj2.shape[1]):
            pygame.draw.circle(
                surface,
                pygame.Color("green"),
                (traj2[0, i, 0, STEP], traj2[0, i, 1, STEP]),
                5)


    draw_particles()
    pygame.display.flip()

    clock = pygame.time.Clock()
    running = True
    started = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    started = True
        if started:
            surface.fill(pygame.Color("black"))
            draw_particles()
            pygame.display.flip()
            if STEP < NUMBER_OF_STEPS:
                STEP += 1
            clock.tick(120)
