import numpy as np
from geometry.primitives import Point, Trapezoid
import geometry.algorithms as algorithms


class StateModel:

    width: int
    height: int

    trapezoid: Trapezoid
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
        pixels = algorithms.get_pixels_with_bresenham(self.start_point, self.end_point)
        # convert np-array to list
        self.set_active_pixels([Point(x, y) for x, y in pixels])

    # setter-methods
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
