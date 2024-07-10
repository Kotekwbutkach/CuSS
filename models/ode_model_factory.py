from typing import Callable

import numpy as np
import pygame

from models import OdeModel


def cucker_smale_function_factory(phi: Callable[[np.ndarray], np.ndarray]):
    def cucker_smale_function(state: np.ndarray):
        n = state.shape[1]

        result = np.zeros(state.shape)
        result[0, :] = state[1, :]

        positions = np.tile(state, n).reshape(2, n, n, 2)
        position_differences = positions.transpose((0, 3, 1, 2)) - positions.transpose((0, 3, 2, 1))
        distance_in_x = np.std(position_differences[0, :], axis=0)
        interaction_strength = np.tile(phi(distance_in_x), 2).reshape(2, n, n)
        difference_in_v = position_differences[1, :]

        pairwise_acceleration = np.multiply(difference_in_v, interaction_strength)
        result[1, :] = np.mean(pairwise_acceleration, axis=1).transpose()
        return result
    return cucker_smale_function


def get_k_subsets(k, n) -> list[[set[int]]]:
    if k == n:
        return [{x for x in range(n)}]
    elif k == 1:
        return [{x} for x in range(n)]
    else:
        return get_k_subsets(k, n-1) + [{*x, n-1} for x in get_k_subsets(k-1, n-1)]


def higher_order_cucker_smale_function_factory(order: int, phi: Callable[[np.ndarray], np.ndarray]):
    def higher_order_cucker_smale_function(state: np.ndarray):
        n = state.shape[1]

        result = np.zeros(state.shape)
        result[0, :] = state[1, :]

        subsets = get_k_subsets(order, n)
        subset_midpoints = np.mean(np.array([[state[:, x, :] for x in g] for g in subsets]), axis=1)
        subset_positions = np.tile(subset_midpoints.transpose(1, 0, 2), n).reshape(2, len(subsets), n, 2)

        positions = np.tile(state, len(subsets)).reshape(2, n, len(subsets), 2)

        position_differences = subset_positions - positions.transpose((0, 2, 1, 3))
        distance_in_x = np.std(position_differences[0, :], axis=2)
        interaction_strength = np.tile(phi(distance_in_x), 2).reshape(len(subsets), n, 2)
        difference_in_v = position_differences[1, :]

        pairwise_acceleration = np.multiply(difference_in_v, interaction_strength)
        result[1, :] = np.mean(pairwise_acceleration, axis=0)
        return result
    return higher_order_cucker_smale_function


class OdeModelFactory:
    def __init__(self):
        pass

    def create_standard(self, time_step: float, phi: Callable[[np.ndarray], np.ndarray]):
        return OdeModel(time_step, cucker_smale_function_factory(phi))

    def create_higher_order(self, time_step: float, order: int, phi: Callable[[np.ndarray], np.ndarray]):
        return OdeModel(time_step, higher_order_cucker_smale_function_factory(order, phi))


if __name__ == "__main__":
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

    factory = OdeModelFactory()
    model1 = factory.create_higher_order(0.05, 3, vector_phi)
    traj1 = model1.calculate_trajectory(initial_condition, NUMBER_OF_STEPS)

    model2 = factory.create_standard(0.05, vector_phi)
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
