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
        self.app = parent # This stores a reference to the Window, so we can interact with the other stuff
        self.state = state # This is our state-store
        self.state.subscribe(self.update_from_state)


        # --- Algorithm selection ---
        tk.Label(self, text="Line Algorithm:").pack(pady=5)
        self.algorithm_var = tk.IntVar(value=LineAlgorithm.BRESENHAM.value)
        for algo in LineAlgorithm:
            tk.Radiobutton(
                self,
                text=algo.name.replace("_", " ").title(),  # Nice display
                variable=self.algorithm_var,
                value=algo.value,
                command=self._update_algorithm
            ).pack(anchor="w")

        # --- Points panel ---
        tk.Label(self, text="Selected Points:").pack(pady=10)

        # Start point
        start_frame = tk.Frame(self)
        start_frame.pack(anchor="w", pady=2)
        tk.Label(start_frame, text="Start:").pack(side="left")
        self.start_x_var = tk.IntVar(value=0)
        self.start_y_var = tk.IntVar(value=0)
        tk.Entry(start_frame, width=4, textvariable=self.start_x_var).pack(side="left")
        tk.Entry(start_frame, width=4, textvariable=self.start_y_var).pack(side="left")

        # End point
        end_frame = tk.Frame(self)
        end_frame.pack(anchor="w", pady=2)
        tk.Label(end_frame, text="End:").pack(side="left")
        self.end_x_var = tk.IntVar(value=0)
        self.end_y_var = tk.IntVar(value=0)
        tk.Entry(end_frame, width=4, textvariable=self.end_x_var).pack(side="left")
        tk.Entry(end_frame, width=4, textvariable=self.end_y_var).pack(side="left")

        # Update button (optional)
        # tk.Button(self, text="Update Line", command=self.update_line).pack(pady=5)

    def _update_algorithm(self):
        self.state.set_algorithm(LineAlgorithm(self.algorithm_var.get()))

    def update_from_state(self) -> None:
        self.algorithm_var = tk.IntVar(value=self.state.algorithm.value)
        self.start_x_var = tk.IntVar(value=self.state.start_point.x)
        self.start_y_var = tk.IntVar(value=self.state.start_point.y)
        self.stop_x_var = tk.IntVar(value=self.state.end_point.x)
        self.stop_y_var = tk.IntVar(value=self.state.end_point.y)
