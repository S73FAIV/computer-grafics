import numpy as np
from geometry.primitives import Point, Trapezoid
from typing import Callable


class StateModel:
    """Holds the current geometric figure and rendering configuration."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

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

        # Independent transformation parameters
        self.translation = np.array([0.0, 0.0])
        self.rotation_deg = 0.0
        self.scale = np.array([1.0, 1.0])
        self.shear = np.array([0.0, 0.0])
        self.reflection = {"enabled": False, "m": 0.0, "t": 0.0}

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

    # --- Transformation setters ---
    def set_translation(self, dx: float, dy: float):
        self.translation = np.array([dx, dy])
        self.update_transformed()

    def set_rotation(self, degrees: float):
        self.rotation_deg = degrees
        self.update_transformed()

    def set_scale(self, sx: float, sy: float):
        self.scale = np.array([sx, sy])
        self.update_transformed()

    def set_shear(self, shear_x: float, shear_y: float):
        """Set shear (skew) angles in degrees and update geometry."""
        self.shear = np.array([shear_x, shear_y])
        self.update_transformed()

    def set_reflection(self, m: float, t: float):
        """Set reflection line parameters (y = m*x + t) and enable reflection."""
        self.reflection["enabled"] = True
        self.reflection["m"] = m
        self.reflection["t"] = t
        self.update_transformed()

    def disable_reflection(self):
        """Turn off reflection."""
        self.reflection["enabled"] = False
        self.update_transformed()

    def update_transformed(self):
        self.transformation_matrix = self._compute_transform_matrix()
        transformed_trapezoid = self.original_trapezoid.transformed(self.transformation_matrix)
        self.set_active_pixels(transformed_trapezoid.active_pixels)

    def _compute_transform_matrix(self) -> np.ndarray:
        """Compute composite 3x3 transformation matrix from stored parameters."""
        dx, dy = self.translation
        angle = np.deg2rad(self.rotation_deg)
        sx, sy = self.scale
        shx, shy = np.deg2rad(self.shear)

        # Translation
        T = np.array([
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1],
        ])

        # Rotation (about origin)
        R = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle),  np.cos(angle), 0],
            [0, 0, 1],
        ])

        # Scaling
        S = np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1],
        ])

        # --- Shear (Skew) matrix ---
        Sh = np.array([[1, np.tan(shx), 0],
                       [np.tan(shy), 1, 0],
                       [0, 0, 1]])

        # Combined: T * R * S
        M = T @ R @ Sh @ S

        # --- Reflection (if enabled) ---
        if self.reflection["enabled"]:
            m = self.reflection["m"]
            t = self.reflection["t"]

            # Convert y = m x + t into reflection matrix
            theta = np.arctan(m)
            c, s = np.cos(theta), np.sin(theta)

            # Translate line to pass through origin (subtract t on Y)
            T1 = np.array([[1, 0, 0],
                           [0, 1, -t],
                           [0, 0, 1]])

            # Rotate line to align with x-axis
            R1 = np.array([[c, s, 0],
                           [-s, c, 0],
                           [0, 0, 1]])

            # Reflect about x-axis
            RefX = np.array([[1, 0, 0],
                             [0, -1, 0],
                             [0, 0, 1]])

            # Inverse rotation & translation
            R2 = np.linalg.inv(R1)
            T2 = np.linalg.inv(T1)

            Ref_line = T2 @ R2 @ RefX @ R1 @ T1
            M = Ref_line @ M

        return M

    # --- State mutators ---
    def update_pixels(self) -> None:
        """Recompute the active pixels from the trapezoid geometry."""
        self.update_transformed()

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
