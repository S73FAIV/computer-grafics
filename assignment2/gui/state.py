import numpy as np
from geometry.primitives import Point, Trapezoid
from typing import Callable


class StateModel:
    """Holds the current geometric figure and rendering configuration."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.canvas_scale = 20

        # Core geometry
        self.original_trapezoid = Trapezoid(
            Point(-8, -2),
            Point(5, -2),
            Point(5, 5),
            Point(-5, 5),
        )

        # Appearance configuration
        self.line_color = "#0000FF"
        self.bg_color = "#EBEBEB"

        # Global transformation matrix
        self.transformation_matrix = np.eye(3)

        # Computed render pixels
        self.active_pixels = self.original_trapezoid.active_pixels
        self.transformation_matrix = np.eye(3)

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

    def apply_matrix(self, M_local: np.ndarray):
        self.transformation_matrix = M_local @ self.transformation_matrix
        self._recompute_pixels()

    def reset_matrix(self):
        self.transformation_matrix = np.eye(3)
        self._recompute_pixels()

    def _recompute_pixels(self):
        transformed = self.original_trapezoid.transformed(self.transformation_matrix)
        self.set_active_pixels(transformed.active_pixels)

    # --- State mutators ---
    def update_pixels(self) -> None:
        """Recompute the active pixels from the trapezoid geometry."""
        # self.update_transformed()
        pass

    def set_active_pixels(self, pixels: list[Point]) -> None:
        self.active_pixels = pixels
        #print("DEBUG: state.set_active_pixels: ", self.active_pixels)
        self.notify()

    def set_line_color(self, color: str) -> None:
        self.line_color = color
        #print("DEBUG: state.line_color: ", self.line_color)
        self.notify()

    def set_bg_color(self, color: str) -> None:
        self.bg_color = color
        #print("DEBUG: state.bg_color: ", self.bg_color)
        self.notify()

    def set_size(self, height: int, width: int) -> None:
        self.width = width
        self.height = height
        print("Update width:", width)
        print("Update height:", height)
        self.notify()

    def set_grid_size(self, scale: int) -> None:
        self.canvas_scale = scale
        self.notify()
