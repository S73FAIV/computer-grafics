import numpy as np
from geometry.primitives import Point, LineAlgorithm


class LineModel:

    width: int
    height: int

    start_point: Point
    end_point: Point
    active_pixels: list[Point]

    def __init__(self, width, height):
        # width and height of the pixel-field in shown? pixels
        self.width = width
        self.height = height

        self.start_point = Point(0, 0)  # centered coordinates
        self.end_point = Point(0, 0)  # centered coordinates
        self.active_pixels = [self.start_point, self.end_point]
        # self.active_pixels = np.zeros((height, width), dtype=bool)  # logical pixel grid
        self.algorithm = LineAlgorithm.BRESENHAM  # LineAlgorithm

        # Subscribers (views)
        self.subscribers = []

    # Subscribe a view
    def subscribe(self, callback) -> None:
        self.subscribers.append(callback)

    # Notify all subscribers of a state change
    def notify(self) -> None:
        for callback in self.subscribers:
            callback()

    # setter-methods
    def set_start_point(self, point: Point) -> None:
        self.start_point = point
        self.active_pixels[0] = point
        print("Update start_point: ", self.start_point)
        self.notify()

    def set_end_point(self, point: Point) -> None:
        self.end_point = point
        self.active_pixels[1] = point
        print("Update end_point: ", self.end_point)
        self.notify()

    def set_algorithm(self, algo: LineAlgorithm) -> None:
        self.algorithm = algo
        print("Update algorithm: ", self.algorithm.name)
        self.notify()

    def set_active_pixels(self, pixels_array: list[Point]) -> None:
        self.active_pixels = pixels_array
        print("Update active_pixels: ", self.active_pixels)
        self.notify()
