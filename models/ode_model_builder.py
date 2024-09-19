from data.aliases import *
from models import OdeModel
from validation import Validate


def get_k_subsets(k, n) -> list[[set[int]]]:
    Validate(k).is_less_than_or_equal(n)
    if k == n:
        return [{x for x in range(n)}]
    elif k == 1:
        return [{x} for x in range(n)]
    else:
        return get_k_subsets(k, n-1) + [{*x, n-1} for x in get_k_subsets(k-1, n-1)]


class OdeModelBuilder:
    phi: ArrayMethod
    distance: ArrayDistanceMethod
    model_factory: Callable[[ArrayMethod, ArrayDistanceMethod], ArrayMethod]

    def __init__(self):
        pass

    def with_default_phi_function(self, c: float = 1, beta: float = 4):
        def __phi(s: float):
            return c / (1 + (s ** (beta/2)))

        _phi = np.vectorize(__phi)
        self.phi = _phi
        return self

    def with_custom_phi_function(self, _phi: Callable[[np.ndarray], np.ndarray]):
        self.phi = _phi
        return self

    def with_default_distance_function(self):
        def _distance(a1: np.ndarray, a2: np.ndarray):
            return np.sqrt(np.sum((a1 - a2) ** 2, axis=0))
        self.distance = _distance
        return self

    def with_modulo_distance_function(self, modulo_bounds: BoundaryInt):
        def _distance(a1: np.ndarray, a2: np.ndarray):
            one_dim_modulo_mask = np.tile(modulo_bounds[1], (5, 5, 1)).transpose(2, 1, 0)
            modulo_adjustments = np.stack(
                [np.stack(
                    (one_dim_modulo_mask[0, :] * i,
                     one_dim_modulo_mask[1, :] * j)
                ) for i in range(-1, 2) for j in range(-1, 2)]
            )
            array_difference = np.tile(a1 - a2, (9, 1, 1, 1))
            distances = array_difference + modulo_adjustments
            return np.min(np.sqrt(np.sum(distances
                                         ** 2, axis=1)), axis=0)
        self.distance = _distance
        return self

    def with_custom_distance_function(self, _distance: ArrayDistanceMethod):
        self.distance = _distance
        return self

    def with_standard_cucker_smale_model(self):
        def cucker_smale_function_factory(phi: ArrayMethod, distance: ArrayDistanceMethod):
            def cucker_smale_function(state: np.ndarray):
                n = state.shape[1]

                result = np.zeros(state.shape)
                result[0, :] = state[1, :]

                positions = np.tile(state, n).reshape(2, n, n, 2)
                distance_in_x = distance(
                    positions.transpose((0, 3, 1, 2))[0, :],
                    positions.transpose((0, 3, 2, 1))[0, :])
                interaction_strength = np.tile(phi(distance_in_x), (2, 1, 1))
                difference_in_v = (positions.transpose((0, 3, 1, 2)) - positions.transpose((0, 3, 2, 1)))[1, :]
                pairwise_acceleration = np.multiply(difference_in_v, interaction_strength)
                result[1, :] = np.mean(pairwise_acceleration, axis=1).transpose()
                return result
            return cucker_smale_function
        self.model_factory = cucker_smale_function_factory
        return self

    def with_higher_order_cucker_smale_model(self, order: int):
        def higher_order_cucker_smale_function_factory(phi: ArrayMethod, distance: ArrayDistanceMethod):
            def higher_order_cucker_smale_function(state: np.ndarray):
                n = state.shape[1]

                result = np.zeros(state.shape)
                result[0, :] = state[1, :]

                subsets = get_k_subsets(order, n)
                subset_midpoints = np.mean(np.array([[state[:, x, :] for x in g] for g in subsets]), axis=1)
                subset_positions = np.tile(subset_midpoints.transpose(1, 0, 2), n).reshape(2, len(subsets), n, 2)

                positions = np.tile(state, len(subsets)).reshape(2, n, len(subsets), 2)

                distance_in_x = distance(
                    positions.transpose((0, 3, 1, 2))[0, :],
                    subset_positions.transpose(0, 3, 2, 1)[0, :])
                interaction_strength = np.tile(phi(distance_in_x), (2, 1, 1))
                difference_in_v = (
                    subset_positions[1, :].transpose(2, 1, 0)
                    - positions[1, :].transpose(2, 0, 1))

                pairwise_acceleration = np.multiply(difference_in_v, interaction_strength)
                result[1, :] = np.mean(pairwise_acceleration, axis=2).transpose(1, 0)
                return result
            return higher_order_cucker_smale_function
        self.model_factory = higher_order_cucker_smale_function_factory
        return self

    def build_for_time_step(self, time_step):
        return OdeModel(time_step, self.model_factory(self.phi, self.distance))
