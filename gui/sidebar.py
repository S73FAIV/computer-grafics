import tkinter as tk
from geometry.primitives import LineAlgorithm, Point
from gui.state import LineModel


class Sidebar(tk.Frame):

    state: LineModel
    algorithm_var: tk.IntVar
    start_x_var: tk.IntVar
    start_y_var: tk.IntVar
    stop_x_var: tk.IntVar
    stop_y_var: tk.IntVar

    def __init__(self, parent, state: LineModel, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = parent  # This stores a reference to the Window, so we can interact with the other stuff
        self.state = state  # This is our state-store
        self.state.subscribe(self.update_from_state)

        # --- Algorithm selection ---
        tk.Label(self, text="Line Algorithm:").pack(pady=5)
        self.algorithm_var = tk.IntVar(value=self.state.algorithm.value)
        for algo in LineAlgorithm:
            tk.Radiobutton(
                self,
                text=algo.name.replace("_", " ").title(),  # Nice display
                variable=self.algorithm_var,
                value=algo.value,
                command=self.update_algorithm,
            ).pack(anchor="w")

        # --- Points panel ---
        tk.Label(self, text="Selected Points:").pack(pady=10)

        # Start point
        start_frame = tk.Frame(self)
        start_frame.pack(anchor="w", pady=2)
        tk.Label(start_frame, text="Start:").pack(side="left")
        self.start_x_var = tk.IntVar(value=0)
        self.start_y_var = tk.IntVar(value=0)
        tk.Spinbox(
            start_frame,
            from_=-(self.state.width / 2),
            to=(self.state.width / 2),
            increment=1,
            textvariable=self.start_x_var,
            width=4,
        ).pack(side="left")
        tk.Spinbox(
            start_frame,
            from_=-(self.state.height / 2),
            to=(self.state.height / 2),
            increment=1,
            textvariable=self.start_y_var,
            width=4,
        ).pack(side="left")
        tk.Button(start_frame, command=self.update_start_point, text="Update").pack(side="left")

        # End point
        end_frame = tk.Frame(self)
        end_frame.pack(anchor="w", pady=2)
        tk.Label(end_frame, text="End:").pack(side="left")
        self.end_x_var = tk.IntVar(value=0)
        self.end_y_var = tk.IntVar(value=0)
        tk.Spinbox(
            end_frame,
            from_=-(self.state.width / 2),
            to=(self.state.width / 2),
            increment=1,
            textvariable=self.end_x_var,
            width=4
        ).pack(side="left")
        tk.Spinbox(
            end_frame,
            from_=-(self.state.height / 2),
            to=(self.state.height / 2),
            increment=1,
            textvariable=self.end_y_var,
            width=4
        ).pack(side="left")
        tk.Button(end_frame, command=self.update_end_point, text="Update").pack(side="left")

        tk.Button(self, text="Draw Line", command=self.draw_line).pack(pady=5)

    def update_from_state(self) -> None:
        self.algorithm_var.set(self.state.algorithm.value)
        self.start_x_var.set(self.state.start_point.x)
        self.start_y_var.set(self.state.start_point.y)
        self.end_x_var.set(self.state.end_point.x)
        self.end_y_var.set(self.state.end_point.y)

    def update_algorithm(self) -> None:
        self.state.set_algorithm(LineAlgorithm(self.algorithm_var.get()))

    def update_start_point(self) -> None:
        self.state.set_start_point(Point(self.start_x_var.get(), self.start_y_var.get()))

    def update_end_point(self) -> None:
        self.state.set_end_point(Point(self.end_x_var.get(), self.end_y_var.get()))

    def draw_line(self) -> None:
        self.state.draw_line()
