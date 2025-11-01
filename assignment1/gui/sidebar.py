import tkinter as tk
from geometry.primitives import LineAlgorithm, Point
from gui.state import LineModel
import tkinter.colorchooser as colorchooser


class Sidebar(tk.Frame):

    state: LineModel
    algorithm_var: tk.IntVar
    start_x_var: tk.IntVar
    start_y_var: tk.IntVar
    stop_x_var: tk.IntVar
    stop_y_var: tk.IntVar
    pixels_text: tk.Text

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

        ## Colours
        tk.Label(self, text="Line Color:").pack(pady=5)
        color_frame = tk.Frame(self)
        color_frame.pack(pady=2, anchor="w")
        self.color_preview = tk.Label(color_frame, bg=self.state.line_color, width=10, height=1)
        self.color_preview.pack(side="left", pady=2)
        tk.Button(color_frame, text="Choose Color", command=self.choose_color).pack(pady=2)

        tk.Label(self, text="Background Color:").pack(pady=5)
        bg_frame = tk.Frame(self)
        bg_frame.pack(pady=2, anchor="w")
        self.bg_preview = tk.Label(bg_frame, bg=self.state.bg_color, width=10, height=1)
        self.bg_preview.pack(side="left", padx=2)
        tk.Button(bg_frame, text="Choose Color", command=self.choose_bg_color).pack(side="left", padx=2)

        # Canvas Size
        size_frame = tk.Frame(self)
        size_frame.pack(anchor="w", pady=2)
        tk.Label(size_frame, text="Canvas Size (height x width):").pack(side="left")
        self.height_var = tk.IntVar(value=0)
        self.width_var = tk.IntVar(value=0)
        tk.Spinbox(
            size_frame,
            from_=10,
            to=400,
            increment=5,
            textvariable=self.height_var,
            width=4
        ).pack(side="left")
        tk.Spinbox(
            size_frame,
            from_=10,
            to=400,
            increment=5,
            textvariable=self.width_var,
            width=4
        ).pack(side="left")
        tk.Button(size_frame, command=self.update_canvas_size, text="Update").pack(side="left")

        # Canvas Size
        scale_frame = tk.Frame(self)
        scale_frame.pack(anchor="w", pady=2)
        tk.Label(scale_frame, text="Pixel-Size").pack(side="left")
        self.scale_var = tk.IntVar(value=0)
        tk.Spinbox(
            scale_frame,
            from_=1,
            to=40,
            increment=1,
            textvariable=self.scale_var,
            width=4
        ).pack(side="left")
        tk.Button(scale_frame, command=self.update_canvas_scale, text="Update").pack(side="left")

        # active pixels
        tk.Label(self, text="Active Pixels:").pack(pady=5)
        self.pixels_text = tk.Text(self, height=10, width=25, state="disabled")
        self.pixels_text.pack(pady=5, fill="x")

    def update_from_state(self) -> None:
        self.algorithm_var.set(self.state.algorithm.value)
        self.start_x_var.set(self.state.start_point.x)
        self.start_y_var.set(self.state.start_point.y)
        self.end_x_var.set(self.state.end_point.x)
        self.end_y_var.set(self.state.end_point.y)
        self.height_var.set(self.state.height)
        self.width_var.set(self.state.width)
        self.scale_var.set(self.state.scale)
        self.color_preview.config(bg=self.state.line_color)
        self.bg_preview.config(bg=self.state.bg_color)
        self.update_pixel_list()

    def update_algorithm(self) -> None:
        self.state.set_algorithm(LineAlgorithm(self.algorithm_var.get()))

    def update_start_point(self) -> None:
        self.state.set_start_point(Point(self.start_x_var.get(), self.start_y_var.get()))

    def update_end_point(self) -> None:
        self.state.set_end_point(Point(self.end_x_var.get(), self.end_y_var.get()))

    def update_pixel_list(self) -> None:
        """Display all active pixels in the text box."""
        self.pixels_text.configure(state="normal")
        self.pixels_text.delete("1.0", tk.END)
        for pixel in self.state.active_pixels:
            self.pixels_text.insert(tk.END, f"({pixel.x}, {pixel.y});")
        self.pixels_text.configure(state="disabled")

    def update_canvas_size(self) -> None:
        self.state.set_size(height=self.height_var.get(), width=self.width_var.get())

    def update_canvas_scale(self) -> None:
        self.state.set_grid_size(self.scale_var.get())

    def draw_line(self) -> None:
        self.state.draw_line()

    def choose_color(self) -> None:
        color_code = colorchooser.askcolor(title="Choose Line Color", color=self.state.line_color)
        if color_code[1]:
            self.state.set_line_color(color_code[1])
            self.color_preview.config(bg=color_code[1])

    def choose_bg_color(self) -> None:
        color_code = colorchooser.askcolor(title="Choose Background Color", color=self.state.bg_color)
        if color_code[1]:
            self.state.set_bg_color(color_code[1])
            self.bg_preview.config(bg=color_code[1])


