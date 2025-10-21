import tkinter as tk
from gui.sidebar import Sidebar
from gui.pixel_frame import PixelFrame
from gui.state import StateModel


class App(tk.Tk):
    """Main application window. Holds state, sidebar (controller panel), and pixel canvas."""

    def __init__(self):
        super().__init__()
        self.title("Graphic Transformation Tool")
        self.geometry("1000x600")

        canvas_width, canvas_height, scale = 30, 30, 20

        # Central application state (Model)
        self.state = StateModel(canvas_width, canvas_height)

        # Sidebar (Controller)
        self.sidebar = Sidebar(self, state=self.state, width=200, bg="lightgray")
        self.sidebar.pack(side="right", fill="y")

        # Canvas (View)
        self.canvas_area = PixelFrame(
            self,
            state=self.state,
            width=canvas_width,
            height=canvas_height,
            scale=scale,
            bg="white",
        )
        self.canvas_area.pack(side="right", fill="both", expand=True)
