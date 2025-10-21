import tkinter as tk
from gui.state import StateModel


class PixelFrame(tk.Frame):
    """Canvas view that renders logical coordinates as a pixel grid."""

    def __init__(self, parent, state: StateModel, width=20, height=20, scale=20, **kwargs):
        super().__init__(parent, **kwargs)
        self.state = state
        self.state.subscribe(self.redraw)

        self.width = width
        self.height = height
        self.scale = scale

        self.img = tk.PhotoImage(width=self.width, height=self.height)
        self.img_big = self.img.zoom(self.scale)

        self.label = tk.Label(self, image=self.img_big)
        self.label.pack()

    def redraw(self) -> None:
        """Rebuild image based on model state."""
        # Background fill
        bg = self.state.bg_color
        for x in range(self.width):
            for y in range(self.height):
                self.img.put(bg, (x, y))

        # Draw figure pixels
        color = self.state.line_color
        for pixel in self.state.active_pixels:
            fx, fy = self.coords_to_frame(pixel.x, pixel.y)
            px, py = fx // self.scale, fy // self.scale
            if 0 <= px < self.width and 0 <= py < self.height:
                self.img.put(color, (px, py))

        self.img_big = self.img.zoom(self.scale)
        self.label.config(image=self.img_big)

    def coords_to_frame(self, x: int, y: int) -> tuple[int, int]:
        """Convert centered logical coordinates to frame coordinates (top-left origin)."""
        logical_x = x + (self.width // 2)
        logical_y = (self.height // 2) - y
        return logical_x * self.scale, logical_y * self.scale
