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


class Line:
    start_point: Point
    end_point: Point
    active_pixels: np.ndarray

    def __init__(
        self, start_point: Point = Point(0, 0), end_point: Point = Point(0, 0)
    ):
        self.start_point = start_point
        self.end_point = end_point

    def draw(self, active_pixels: np.ndarray) -> None:
        self.active_pixels = active_pixels


class Trapezoid:

    # TODO: decide on representation -> Points or lines?!
    A: Point  # lower left
    B: Point  # lower right
    C: Point  # upper right
    D: Point  # upper left

    # The points are connected by the lines:
    AB: Line
    BC: Line
    CD: Line
    DA: Line

    def __init__(self, A: Point, B: Point, C: Point, D: Point) -> None:
        self.A = A
        self.B = B
        self.C = C
        self.D = D

        self.AB = Line(A, B)
        self.BC = Line(B, C)
        self.CD = Line(C, D)
        self.DA = Line(D, A)
