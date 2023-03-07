from math import pi
from random import uniform


def get_random_vec2(a: float = -2.0, b: float = 2.0):
    return tuple(uniform(a, b) for _ in range(2))


def get_random_vec3(a: float = -2.0, b: float = 2.0):
    return tuple(uniform(a, b) for _ in range(3))


def get_random_angle() -> float:
    return uniform(0, 2 * pi)
