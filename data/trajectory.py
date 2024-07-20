import numpy as np
from data.aliases import *


class Trajectory:
    data: np.ndarray
    torus_bounds: BoundaryFloat | None

    def __init__(self, data: np.ndarray, torus_bounds: BoundaryFloat = None):
        self.data = data
        self.torus_bounds = torus_bounds
