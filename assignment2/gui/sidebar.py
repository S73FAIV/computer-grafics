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

        # --- Figure info ---
        tk.Label(self, text="Corner Points:").pack(pady=(10, 5))
        self.pixels_text = tk.Text(self, height=8, width=25, state="disabled")
        self.pixels_text.pack(pady=5, fill="x")

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
