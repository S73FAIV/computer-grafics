import numpy as np
from geometry.primitives import Point, LineAlgorithm
import geometry.algorithms as algorithms


class LineModel:

    width: int
    height: int

    start_point: Point
    end_point: Point
    line_color: str
    bg_color: str
    active_pixels: list[Point]

    def __init__(self, width, height):
        # width and height of the pixel-field in shown? pixels
        self.width = width
        self.height = height

        self.start_point = Point(0, 0)  # centered coordinates
        self.end_point = Point(0, 0)  # centered coordinates
        self.line_color = "#0000FF"
        self.bg_color = "#ebebeb"
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

    def draw_line(self) -> None:
        pixels = []
        if self.algorithm == LineAlgorithm.SLOPE_INTERCEPT:
            pixels = algorithms.get_pixels_with_slope_intercept(self.start_point, self.end_point)
        elif self.algorithm == LineAlgorithm.DDA:
            pixels = algorithms.get_pixels_with_dda(self.start_point, self.end_point)
        elif self.algorithm == LineAlgorithm.BRESENHAM:
            pixels = algorithms.get_pixels_with_bresenham(self.start_point, self.end_point)
        # convert np-array to list
        self.set_active_pixels([Point(x, y) for x, y in pixels])

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

    def set_line_color(self, color: str) -> None:
        self.line_color = color
        print("Update line_color: ", color)
        self.notify()

    def set_bg_color(self, color: str) -> None:
        self.bg_color = color
        print("Update bg_color:", color)
        self.notify()

