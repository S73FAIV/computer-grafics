import tkinter as tk
import numpy as np
from geometry.primitives import Point, Line
from gui.state import LineModel


class PixelFrame(tk.Frame):
    width: int
    height: int
    scale: int

    state: LineModel

    selecting_start = True

    def __init__(self, parent, state: LineModel, width=20, height=20, scale=20, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = parent  # This stores a reference to the Window, so we can interact with the other stuff
        self.state = state # This is our state-store
        self.state.subscribe(self.redraw)

        self.width = width
        self.height = height
        self.scale = scale

        # Base logical image
        self.img = tk.PhotoImage(width=self.width, height=self.height)
        self.img_big = self.img.zoom(self.scale)

        # Label for image
        self.label = tk.Label(self, image=self.img_big)
        self.label.pack()

        # Bind click events
        self.label.bind("<Button-1>", self.on_click)

    def set_pixel(self, x, y, color):
        """Update one logical pixel and refresh display."""
        self.img.put(color, (x, y))
        self.refresh_display()

    def refresh_display(self):
        """Recreate the zoomed image after pixel updates."""
        self.img_big = self.img.zoom(self.scale)
        self.label.config(image=self.img_big)

    def on_click(self, event):
        # Convert the clicked frame position to centered coordinates
        x_centered, y_centered = self.frame_to_coords(event.x, event.y)

        if self.selecting_start:
            self.state.set_start_point(Point(x_centered, y_centered))
            print(f"Start point set: {self.state.start_point}")
        else:
            self.state.set_end_point(Point(x_centered, y_centered))
            print(f"End point set: {self.state.end_point}")

        # Toggle selection for next click
        self.selecting_start = not self.selecting_start

        # redraw canvas
        self.redraw()

    def redraw(self) -> None:
        self.img = tk.PhotoImage(width=self.width, height=self.height)

        # Fill background
        for x in range(self.width):
            for y in range(self.height):
                self.img.put(self.state.bg_color, (x, y))

        # Draw line pixels
        color = self.state.line_color
        for pixel in self.state.active_pixels:
            frame_x, frame_y = self.coords_to_frame(pixel.x, pixel.y)
            px, py = frame_x // self.scale, frame_y // self.scale
            if 0 <= px < self.width and 0 <= py < self.height:
                self.img.put(color, (px, py))

        self.img_big = self.img.zoom(self.scale)
        self.label.config(image=self.img_big)

    ####
    # Canvas Position Transformation
    ####
    def frame_to_coords(self, x, y) -> tuple[int, int]:
        """
        Convert frame coordinates (pixels, top-left origin) to centered logical coordinates.
        """
        # convert frame pixels to logical pixels
        logical_x = x // self.scale
        logical_y = y // self.scale

        # shift origin to center
        centered_x = logical_x - (self.width // 2)
        centered_y = (self.height // 2) - logical_y  # y inverted so positive is “up”

        return centered_x, centered_y

    def coords_to_frame(self, x, y) -> tuple[int, int]:
        """
        Convert centered logical coordinates to frame coordinates (pixels, top-left origin).
        """
        # shift origin back to top-left
        logical_x = x + (self.width // 2)
        logical_y = (self.height // 2) - y  # invert y

        # scale up to frame pixels
        x = logical_x * self.scale
        y = logical_y * self.scale

        return x, y

    def frame_to_coords_vec(self, points: np.ndarray) -> np.ndarray:
        """
        Convert array of frame coordinates (pixels, top-left origin) to centered logical coordinates.

        Parameters
        ----------
        points : np.ndarray
            Shape (N,2), columns are [x_frame, y_frame]

        Returns
        -------
        np.ndarray
            Shape (N,2), columns are [x_centered, y_centered]
        """
        # Divide by scale to get logical pixels
        logical = points // self.scale

        # Shift origin to center and invert y
        logical[:, 0] = logical[:, 0] - (self.width // 2)
        logical[:, 1] = (self.height // 2) - logical[:, 1]

        return logical

    def coords_to_frame_vec(self, coords: np.ndarray) -> np.ndarray:
        """
        Convert array of centered logical coordinates to frame coordinates (pixels).

        Parameters
        ----------
        coords : np.ndarray
            Shape (N,2), columns are [x_centered, y_centered]

        Returns
        -------
        np.ndarray
            Shape (N,2), columns are [x_frame, y_frame]
        """
        # Shift origin back to top-left and invert y
        frame = np.empty_like(coords)
        frame[:, 0] = coords[:, 0] + (self.width // 2)
        frame[:, 1] = (self.height // 2) - coords[:, 1]

        # Scale up to frame pixels
        frame *= self.scale
        return frame
