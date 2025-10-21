import numpy as np
from geometry.primitives import Point, Trapezoid


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

        self.trapezoid = Trapezoid(Point(-8, -2), Point(5, -2), Point(5, 5), Point(-5, 5))

        self.line_color = "#0000FF"
        self.bg_color = "#ebebeb"
        self.active_pixels = self.trapezoid.active_pixels

        # Subscribers (views)
        self.subscribers = []

    # Subscribe a view
    def subscribe(self, callback) -> None:
        self.subscribers.append(callback)

    # Notify all subscribers of a state change
    def notify(self) -> None:
        for callback in self.subscribers:
            callback()

    def update_pixels(self) -> None:
        self.set_active_pixels(self.trapezoid.active_pixels)

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
