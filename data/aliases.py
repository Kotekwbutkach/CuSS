from typing import Callable

import numpy as np

PointFloat = tuple[float, float]
PointInt = tuple[float, float]
NullablePointFloat = tuple[float | None, float | None]

BoundaryFloat = tuple[PointFloat, PointFloat]
BoundaryInt = tuple[PointInt, PointInt]
NullableBoundaryFloat = tuple[NullablePointFloat, NullablePointFloat]

ArrayMethod = Callable[[np.ndarray], np.ndarray]
ArrayDistanceMethod = Callable[[np.ndarray, np.ndarray], np.ndarray]