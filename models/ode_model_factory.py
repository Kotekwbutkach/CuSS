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

    @staticmethod
    def create_standard(time_step: float, phi: Callable[[np.ndarray], np.ndarray]):
        return OdeModel(time_step, cucker_smale_function_factory(phi))

    @staticmethod
    def create_higher_order(time_step: float, order: int, phi: Callable[[np.ndarray], np.ndarray]):
        return OdeModel(time_step, higher_order_cucker_smale_function_factory(order, phi))
