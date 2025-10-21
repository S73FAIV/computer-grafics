from enum import Enum
import numpy as np


class Point:
    coords: np.ndarray  # we store the coordinates as numpy array

    def __init__(self, x: int, y: int):
        self.coords = np.array([x, y], dtype=int)

    @property
    def x(self) -> int:
        return self.coords[0]

    @property
    def y(self) -> int:
        return self.coords[1]

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class LineAlgorithm(Enum):
    SLOPE_INTERCEPT = 0
    DDA = 1
    BRESENHAM = 2


class Line:
    start_point: Point
    end_point: Point
    active_pixels: np.ndarray
    creation_algorithm = LineAlgorithm.BRESENHAM

    def __init__(
        self,
        start_point: Point = Point(0, 0),
        end_point: Point = Point(0, 0),
        creation_algorithm: LineAlgorithm = LineAlgorithm.BRESENHAM,
    ):
        self.start_point = start_point
        self.end_point = end_point
        self.creation_algorithm = creation_algorithm

    def draw(self, active_pixels: np.ndarray) -> None:
        self.active_pixels = active_pixels
