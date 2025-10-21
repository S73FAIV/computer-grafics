import tkinter as tk
import numpy as np
from gui.state import StateModel


class PixelFrame(tk.Frame):
    width: int
    height: int
    scale: int

    state: StateModel

    def __init__(
        self, parent, state: StateModel, width=20, height=20, scale=20, **kwargs
    ):
        super().__init__(parent, **kwargs)
        self.app = parent  # This stores a reference to the Window, so we can interact with the other stuff
        self.state = state  # This is our state-store
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

