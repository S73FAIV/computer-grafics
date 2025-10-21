import tkinter as tk
from gui.sidebar import Sidebar
from gui.pixel_frame import PixelFrame
from gui.state import StateModel


class App(tk.Tk):

    state: StateModel  # our state
    sidebar: Sidebar
    canvas_area: PixelFrame

    def __init__(self):
        super().__init__()
        self.title("Grafic Transormation Tool")
        self.geometry("1000x600")

        # canvas-size
        canvas_width, canvas_height, scale = 30, 30, 20

        self.state = StateModel(canvas_width, canvas_height)

        # Sidebar on the right
        self.sidebar = Sidebar(parent=self, state=self.state, width=200, bg="lightgray")
        self.sidebar.pack(side="right", fill="y")

        # Canvas on the right
        self.canvas_area = PixelFrame(
            parent=self,
            state=self.state,
            width=canvas_width,
            height=canvas_height,
            scale=scale,
            bg="white",
        )
        self.canvas_area.pack(side="right", fill="both", expand=True)
