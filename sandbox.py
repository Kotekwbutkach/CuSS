import numpy as np
import pygame

from calculation import ParticlesSystemCalculator
from data import ParticlesSystem
from models import ConstantAccelerationModel
from presentation import Presenter, VelocityPresenter

if __name__ == "__main__":
    number_of_particles = 5
    number_of_dimensions = 2
    step_limit = 200

    particles_system_args = {
        "number_of_particles": number_of_particles,
        "number_of_dimensions": number_of_dimensions,
        "step_limit": step_limit,
        "particles": np.array([[
            [x + 10 * y] * number_of_dimensions +
            [x + 2 * y] * number_of_dimensions +
            [0] * number_of_dimensions for x in range(step_limit)] for y in range(number_of_particles)])}

    particles_system = ParticlesSystem(**particles_system_args)
    model = ConstantAccelerationModel()

    particles_system_calculator = ParticlesSystemCalculator(particles_system, model, 0.1)
    particles_system_calculator.calculate()

    presenter = VelocityPresenter(particles_system)
    # <\setup>

    pygame.init()

    pygame.display.set_mode((800, 600))
    surface = pygame.display.get_surface()
    pygame.display.set_caption('CuSS')
    # TODO pygame.display.set_icon()

    clock = pygame.time.Clock()
    running = True

    step = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        surface.fill(pygame.Color("black"))
        presenter._present_step(surface, step)
        pygame.display.flip()
        if step < particles_system.step_limit - 1:
            step += 1
        clock.tick(20)
