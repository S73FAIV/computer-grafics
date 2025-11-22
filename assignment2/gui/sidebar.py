import tkinter as tk
import tkinter.colorchooser as colorchooser
from gui.state import StateModel
import numpy as np


class Sidebar(tk.Frame):
    """Controller panel to display geometry info and trigger state changes."""

    def __init__(self, parent, state: StateModel, **kwargs):
        super().__init__(parent, **kwargs)
        self.state = state
        self.state.subscribe(self.update_from_state)

        # # Draw figure
        # tk.Button(self, text="(Re)Draw Figure", command=self.redraw_figure).pack(pady=5)
        # --- Figure info ---
        tk.Label(self, text="Info").pack(pady=(10, 5))
        self.pixels_text = tk.Text(self, height=10, width=25, state="disabled")
        self.pixels_text.pack(pady=5, fill="x")

        # Apply button
        tk.Button(self, text="Reset Transforms", command=self.reset_transform).pack(pady=5)

        # --- Translation controls ---
        tk.Label(self, text="Translation:").pack(pady=(10, 5))
        trans_frame = tk.Frame(self)
        trans_frame.pack(pady=2, anchor="w")

        tk.Label(trans_frame, text="dx:").pack(side="left")
        self.dx_var = tk.DoubleVar(value=0.0)
        tk.Spinbox(
            trans_frame,
            from_=-20,
            to=20,
            increment=1,
            textvariable=self.dx_var,
            width=6,
        ).pack(side="left", padx=2)

        tk.Label(trans_frame, text="dy:").pack(side="left")
        self.dy_var = tk.DoubleVar(value=0.0)
        tk.Spinbox(
            trans_frame,
            from_=-20,
            to=20,
            increment=1,
            textvariable=self.dy_var,
            width=6,
        ).pack(side="left", padx=2)
        # Apply button
        tk.Button(trans_frame, text="Apply Transl.", command=self.apply_translation).pack(pady=5)
        
        # --- Rotation controls ---
        tk.Label(self, text="Rotation:").pack(pady=(10, 5))

        rot_frame = tk.Frame(self)
        rot_frame.pack(pady=2, anchor="w")

        tk.Label(rot_frame, text="Angle (°):").pack(side="left")
        self.rot_var = tk.DoubleVar(value=0.0)
        tk.Spinbox(
            rot_frame,
            from_=-360,
            to=360,
            increment=1,
            textvariable=self.rot_var,
            width=6,
        ).pack(side="left", padx=2)

        # Checkbox for counter-clockwise
        self.ccw_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            rot_frame, text="CCW", variable=self.ccw_var, onvalue=True, offvalue=False
        ).pack(side="left", padx=4)
        # Apply button
        tk.Button(rot_frame, text="Apply Rot.", command=self.apply_rotation).pack(pady=5)
        
        # --- Scaling controls ---
        tk.Label(self, text="Scaling:").pack(pady=(10, 5))

        scale_frame = tk.Frame(self)
        scale_frame.pack(pady=2, anchor="w")

        tk.Label(scale_frame, text="sx:").pack(side="left")
        self.sx_var = tk.DoubleVar(value=1.0)
        tk.Spinbox(
            scale_frame,
            from_=0.1,
            to=5.0,
            increment=0.1,
            textvariable=self.sx_var,
            width=6,
        ).pack(side="left", padx=2)

        tk.Label(scale_frame, text="sy:").pack(side="left")
        self.sy_var = tk.DoubleVar(value=1.0)
        tk.Spinbox(
            scale_frame,
            from_=0.1,
            to=5.0,
            increment=0.1,
            textvariable=self.sy_var,
            width=6,
        ).pack(side="left", padx=2)
        # Apply button
        tk.Button(scale_frame, text="Apply Scale", command=self.apply_scaling).pack(pady=5)
        
        # --- Skew controls ---
        tk.Label(self, text="Skew (Shear):").pack(pady=(10, 5))

        shear_frame = tk.Frame(self)
        shear_frame.pack(pady=2, anchor="w")

        tk.Label(shear_frame, text="shx (°):").pack(side="left")
        self.shx_var = tk.DoubleVar(value=0.0)
        tk.Spinbox(
            shear_frame,
            from_=-60,
            to=60,
            increment=1,
            textvariable=self.shx_var,
            width=6,
        ).pack(side="left", padx=2)

        tk.Label(shear_frame, text="shy (°):").pack(side="left")
        self.shy_var = tk.DoubleVar(value=0.0)
        tk.Spinbox(
            shear_frame,
            from_=-60,
            to=60,
            increment=1,
            textvariable=self.shy_var,
            width=6,
        ).pack(side="left", padx=2)
        # Apply button
        tk.Button(shear_frame, text="Apply Skew", command=self.apply_shear).pack(pady=5)
        
        # --- Reflection controls ---
        tk.Label(self, text="Reflection (y = m*x + t):").pack(pady=(10, 5))

        refl_frame = tk.Frame(self)
        refl_frame.pack(pady=2, anchor="w")

        tk.Label(refl_frame, text="m:").pack(side="left")
        self.ref_m_var = tk.DoubleVar(value=0.0)
        tk.Spinbox(
            refl_frame,
            from_=-5.0,
            to=5.0,
            increment=0.1,
            textvariable=self.ref_m_var,
            width=6,
        ).pack(side="left", padx=2)

        tk.Label(refl_frame, text="t:").pack(side="left")
        self.ref_t_var = tk.DoubleVar(value=0.0)
        tk.Spinbox(
            refl_frame,
            from_=-20.0,
            to=20.0,
            increment=0.5,
            textvariable=self.ref_t_var,
            width=6,
        ).pack(side="left", padx=2)
        # Apply button
        tk.Button(refl_frame, text="Apply Refl.", command=self.apply_reflection).pack(pady=5)
        tk.Button(self, text="Reflect on x=0", command=self.apply_reflection_x).pack(pady=5)
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
            width=4,
        ).pack(side="left")
        tk.Spinbox(
            size_frame,
            from_=10,
            to=400,
            increment=5,
            textvariable=self.width_var,
            width=4,
        ).pack(side="left")
        tk.Button(size_frame, command=self.update_canvas_size, text="Update").pack(
            side="left"
        )

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
            width=4,
        ).pack(side="left")
        tk.Button(scale_frame, command=self.update_canvas_scale, text="Update").pack(
            side="left"
        )

        # --- Color pickers ---
        tk.Label(self, text="Colors:").pack(pady=(10, 5))

        color_frame = tk.Frame(self)
        color_frame.pack(pady=2, anchor="w")
        self.color_preview = tk.Label(
            color_frame, bg=self.state.line_color, width=10, height=1
        )
        self.color_preview.pack(side="left", padx=2)
        tk.Button(color_frame, text="Line", command=self.choose_line_color).pack(
            side="left", padx=2
        )

        bg_frame = tk.Frame(self)
        bg_frame.pack(pady=2, anchor="w")
        self.bg_preview = tk.Label(bg_frame, bg=self.state.bg_color, width=10, height=1)
        self.bg_preview.pack(side="left", padx=2)
        tk.Button(bg_frame, text="Background", command=self.choose_bg_color).pack(
            side="left", padx=2
        )

    # --- Event handlers ---
    def choose_line_color(self) -> None:
        color = colorchooser.askcolor(
            title="Choose Line Color", color=self.state.line_color
        )[1]
        if color:
            self.state.set_line_color(color)
            self.color_preview.config(bg=color)

    def choose_bg_color(self) -> None:
        color = colorchooser.askcolor(
            title="Choose Background Color", color=self.state.bg_color
        )[1]
        if color:
            self.state.set_bg_color(color)
            self.bg_preview.config(bg=color)

    def apply_translation(self):
        dx = self.dx_var.get()
        dy = self.dy_var.get()
        M = np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1]])
        self.state.apply_matrix(M)

    def apply_rotation(self):
        angle = self.rot_var.get()
        if not self.ccw_var.get():
            angle = -angle
        a = np.deg2rad(angle)
        M = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
        self.state.apply_matrix(M)

    def apply_scaling(self) -> None:
        sx = self.sx_var.get()
        sy = self.sy_var.get()
        M = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
        self.state.apply_matrix(M)

    def apply_shear(self) -> None:
        shx = np.deg2rad(self.shx_var.get())
        shy = np.deg2rad(self.shy_var.get())
        M = np.array([[1, np.tan(shx), 0], [np.tan(shy), 1, 0], [0, 0, 1]])
        self.state.apply_matrix(M)

    def apply_reflection(self) -> None:
        m = self.ref_m_var.get()
        t = self.ref_t_var.get()

        theta = np.arctan(m)
        c, s = np.cos(theta), np.sin(theta)

        T1 = np.array([[1, 0, 0], [0, 1, -t], [0, 0, 1]])

        R1 = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]])

        RefX = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]])

        R2 = np.linalg.inv(R1)
        T2 = np.linalg.inv(T1)

        M = T2 @ R2 @ RefX @ R1 @ T1

        self.state.apply_matrix(M)

    def apply_reflection_x(self):
        """
        Reflect the figure across the vertical axis x = 0.
        Matrix form:
            [ -1   0   0 ]
            [  0   1   0 ]
            [  0   0   1 ]
        """
        M = np.array([
            [-1,  0, 0],
            [ 0,  1, 0],
            [ 0,  0, 1],
        ])
        self.state.apply_matrix(M)


    def reset_transform(self):
        self.state.reset_matrix()

    def update_canvas_size(self) -> None:
        self.state.set_size(height=self.height_var.get(), width=self.width_var.get())

    def update_canvas_scale(self) -> None:
        self.state.set_grid_size(self.scale_var.get())

    # --- State update ---
    def update_from_state(self) -> None:
        self.color_preview.config(bg=self.state.line_color)
        self.bg_preview.config(bg=self.state.bg_color)
        self._update_corner_list()

    def _update_corner_list(self) -> None:
        """Display original corner points and current transformation matrix."""
        self.pixels_text.configure(state="normal")
        self.pixels_text.delete("1.0", tk.END)

        self.pixels_text.insert(tk.END, "Original corners:\n")
        for p in self.state.original_trapezoid.corners:
            self.pixels_text.insert(tk.END, f"({p.x}, {p.y})\n")

        self.pixels_text.insert(tk.END, "\nTransformation matrix:\n")
        mat = self.state.transformation_matrix
        for row in mat:
            self.pixels_text.insert(
                tk.END, f"{row[0]:7.3f} {row[1]:7.3f} {row[2]:7.3f}\n"
            )

        self.pixels_text.configure(state="disabled")
