import tkinter as tk
from geometry.primitives import Point
from gui.state import StateModel
import tkinter.colorchooser as colorchooser


class Sidebar(tk.Frame):

    state: StateModel
    pixels_text: tk.Text

    def __init__(self, parent, state: StateModel, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = parent  # This stores a reference to the Window, so we can interact with the other stuff
        self.state = state  # This is our state-store
        self.state.subscribe(self.update_from_state)

        # corners of figure
        tk.Label(self, text="Active Pixels:").pack(pady=5)
        self.pixels_text = tk.Text(self, height=10, width=25, state="disabled")
        self.pixels_text.pack(pady=5, fill="x")

    def update_from_state(self) -> None:
        self.update_pixel_list()

    def update_pixel_list(self) -> None:
        """Display all active pixels in the text box."""
        self.pixels_text.configure(state="normal")
        self.pixels_text.delete("1.0", tk.END)
        for pixel in self.state.active_pixels:
            self.pixels_text.insert(tk.END, f"({pixel.x}, {pixel.y});")
        self.pixels_text.configure(state="disabled")

    def draw_line(self) -> None:
        self.state.draw_line()
