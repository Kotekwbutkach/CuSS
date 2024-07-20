import numpy as np

Point = tuple[float, float]
Boundary = tuple[Point, Point]


class Trajectory:
    data: np.ndarray
    torus_bounds: None | Boundary

    def __init__(self, data: np.ndarray, torus_bounds = None):
        self.data = data
        self.torus_bounds = torus_bounds
