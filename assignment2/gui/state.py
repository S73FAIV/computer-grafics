import numpy as np
from geometry.primitives import Point, Trapezoid
from typing import Callable


class StateModel:
    """Holds the current geometric figure and rendering configuration."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        # Core geometry
        self.trapezoid = Trapezoid(
            Point(-8, -2),
            Point(5, -2),
            Point(5, 5),
            Point(-5, 5),
        )

        # Appearance configuration
        self.line_color = "#0000FF"
        self.bg_color = "#EBEBEB"

        # Computed render pixels
        self.active_pixels = self.trapezoid.active_pixels

        # Subscriber callbacks (the Views)
        self._subscribers: list[Callable] = []

    # --- Observer pattern interface ---
    def subscribe(self, callback) -> None:
        """Register a view callback for state updates."""
        self._subscribers.append(callback)

    def notify(self) -> None:
        """Notify all subscribed views of a state change."""
        for callback in self._subscribers:
            callback()

    # --- State mutators ---
    def update_pixels(self) -> None:
        """Recompute the active pixels from the trapezoid geometry."""
        self.set_active_pixels(self.trapezoid.active_pixels)

    def set_active_pixels(self, pixels: list[Point]) -> None:
        self.active_pixels = pixels
        print("DEBUG: state.set_active_pixels: ", self.active_pixels)
        self.notify()

    def set_line_color(self, color: str) -> None:
        self.line_color = color
        print("DEBUG: state.line_color: ", self.line_color)
        self.notify()

    def set_bg_color(self, color: str) -> None:
        self.bg_color = color
        print("DEBUG: state.bg_color: ", self.bg_color)
        self.notify()
