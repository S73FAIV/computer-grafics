import tkinter as tk
import tkinter.colorchooser as colorchooser
from gui.state import StateModel


class Sidebar(tk.Frame):
    """Controller panel to display geometry info and trigger state changes."""

    def __init__(self, parent, state: StateModel, **kwargs):
        super().__init__(parent, **kwargs)
        self.state = state
        self.state.subscribe(self.update_from_state)

        # Draw figure
        tk.Button(self, text="(Re)Draw Figure", command=self.state.update_pixels).pack(pady=5)
        # --- Figure info ---
        tk.Label(self, text="Corner Points:").pack(pady=(10, 5))
        self.pixels_text = tk.Text(self, height=2, width=25, state="disabled")
        self.pixels_text.pack(pady=5, fill="x")

        # --- Translation controls ---
        tk.Label(self, text="Translation:").pack(pady=(10, 5))
        trans_frame = tk.Frame(self)
        trans_frame.pack(pady=2, anchor="w")

        tk.Label(trans_frame, text="dx:").pack(side="left")
        self.dx_var = tk.DoubleVar(value=0.0)
        tk.Spinbox(trans_frame, from_=-20, to=20, increment=1, textvariable=self.dx_var, width=6).pack(side="left", padx=2)

        tk.Label(trans_frame, text="dy:").pack(side="left")
        self.dy_var = tk.DoubleVar(value=0.0)
        tk.Spinbox(trans_frame, from_=-20, to=20, increment=1, textvariable=self.dy_var, width=6).pack(side="left", padx=2)

        tk.Button(self, text="Apply Translation", command=self.apply_translation).pack(pady=5)

        # --- Rotation controls ---
        tk.Label(self, text="Rotation:").pack(pady=(10, 5))

        rot_frame = tk.Frame(self)
        rot_frame.pack(pady=2, anchor="w")

        tk.Label(rot_frame, text="Angle (°):").pack(side="left")
        self.rot_var = tk.DoubleVar(value=0.0)
        tk.Spinbox(rot_frame, from_=-360, to=360, increment=1,
                textvariable=self.rot_var, width=6).pack(side="left", padx=2)

        # Checkbox for counter-clockwise
        self.ccw_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            rot_frame,
            text="CCW",
            variable=self.ccw_var,
            onvalue=True,
            offvalue=False
        ).pack(side="left", padx=4)

        tk.Button(self, text="Apply Rotation", command=self.apply_rotation).pack(pady=5)

        # --- Color pickers ---
        tk.Label(self, text="Colors:").pack(pady=(10, 5))

        color_frame = tk.Frame(self)
        color_frame.pack(pady=2, anchor="w")
        self.color_preview = tk.Label(color_frame, bg=self.state.line_color, width=10, height=1)
        self.color_preview.pack(side="left", padx=2)
        tk.Button(color_frame, text="Line", command=self.choose_line_color).pack(side="left", padx=2)

        bg_frame = tk.Frame(self)
        bg_frame.pack(pady=2, anchor="w")
        self.bg_preview = tk.Label(bg_frame, bg=self.state.bg_color, width=10, height=1)
        self.bg_preview.pack(side="left", padx=2)
        tk.Button(bg_frame, text="Background", command=self.choose_bg_color).pack(side="left", padx=2)


    # --- Event handlers ---
    def choose_line_color(self) -> None:
        color = colorchooser.askcolor(title="Choose Line Color", color=self.state.line_color)[1]
        if color:
            self.state.set_line_color(color)
            self.color_preview.config(bg=color)

    def choose_bg_color(self) -> None:
        color = colorchooser.askcolor(title="Choose Background Color", color=self.state.bg_color)[1]
        if color:
            self.state.set_bg_color(color)
            self.bg_preview.config(bg=color)

    def apply_translation(self):
        dx = self.dx_var.get()
        dy = self.dy_var.get()
        self.state.set_translation(dx, dy)

    def apply_rotation(self) -> None:
        angle = self.rot_var.get()
        if not self.ccw_var.get():  # clockwise → negate
            angle = -angle
        self.state.set_rotation(angle)

    # --- State update ---
    def update_from_state(self) -> None:
        self.color_preview.config(bg=self.state.line_color)
        self.bg_preview.config(bg=self.state.bg_color)
        self._update_corner_list()

    def _update_corner_list(self) -> None:
        """Display trapezoid corner coordinates."""
        text = "; ".join(f"({p.x}, {p.y})" for p in self.state.trapezoid.corners)
        self.pixels_text.configure(state="normal")
        self.pixels_text.delete("1.0", tk.END)
        self.pixels_text.insert(tk.END, text)
        self.pixels_text.configure(state="disabled")
