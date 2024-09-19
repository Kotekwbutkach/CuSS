import unittest

import numpy as np

from models import OdeModel

# data preparation

TIME_STEP = 0.1
NUMBER_OF_PARTICLES = 5
STEPS_LIMIT = 50


def _test_identity_function(array: np.ndarray):
    return np.zeros(array.shape)


def _test_constant_function(array: np.ndarray):
    result = np.zeros(array.shape)
    result[0, :] = array[1, :]
    result[1, :] = np.zeros(array[1, :].shape)
    return result

# /data preparation


class TestOdeModel(unittest.TestCase):
    def test_identity_model_returns_correct_trajectory(self):
        model = OdeModel(TIME_STEP, _test_identity_function)

        initial_data = np.random.normal(0, 1, 4 * NUMBER_OF_PARTICLES).reshape(2, -1, 2)
        result = model.calculate_trajectory(initial_data, STEPS_LIMIT)
        for t in range(STEPS_LIMIT):
            np.testing.assert_array_equal(initial_data, result[:, :, t])

    def test_constant_model_returns_correct_trajectory(self):
        model = OdeModel(TIME_STEP, _test_constant_function)

        initial_data = np.random.normal(0, 1, 4 * NUMBER_OF_PARTICLES).reshape(2, -1, 2)
        result = model.calculate_trajectory(initial_data, STEPS_LIMIT)
        for t in range(STEPS_LIMIT):
            state = initial_data
            state[0, :] = (t+1) * initial_data[0, :]
            np.testing.assert_array_equal(initial_data, state)


if __name__ == '__main__':
    unittest.main()
