from typing import Union, Tuple

import numpy as np


class Validate:
    value: object

    def __init__(self, value: object):
        self.value = value

    def is_type(self, checked_type: type):
        if isinstance(self.value, checked_type):
            return
        raise TypeError(f"Value {self.value} is not of type {checked_type}")

    def is_less_than(self, checked_value: Union[float, int]):
        if isinstance(self.value, float) and self.value < float(checked_value):
            return
        if isinstance(self.value, int) and self.value < int(checked_value):
            return
        raise ValueError(f"Value {self.value} should be less than {checked_value}")

    def is_less_than_or_equal(self, checked_value: Union[float, int]):
        if isinstance(self.value, float) and self.value <= float(checked_value):
            return
        if isinstance(self.value, int) and self.value <= int(checked_value):
            return
        raise ValueError(f"Value {self.value} should not be greater than {checked_value}")

    def is_greater_than(self, checked_value: Union[float, int]):
        if isinstance(self.value, float) and self.value > float(checked_value):
            return
        if isinstance(self.value, int) and self.value > int(checked_value):
            return
        raise ValueError(f"Value {self.value} should be greater than {checked_value}")

    def is_greater_than_or_equal(self, checked_value: Union[float, int]):
        if isinstance(self.value, float) and self.value >= float(checked_value):
            return
        if isinstance(self.value, int) and self.value >= int(checked_value):
            return
        raise ValueError(f"Value {self.value} should not be less than {checked_value}")

    def is_of_shape(self, checked_shape: Tuple[int, ...]):
        if isinstance(self.value, np.ndarray) and self.value.shape == checked_shape:
            return
        raise ValueError(f"Array {self.value} is not of expected shape {checked_shape}")
