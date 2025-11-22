# Graphics and Virtual Reality — Assignment Collection

University of Cantabria
**Gráficos por Computador y Realidad Virtual**

This repository contains the full set of four practical assignments developed for the course **Gráficos por Computador y Realidad Virtual** at the **University of Cantabria**.
All assignments are implemented in **Python**, using a consistent project structure and optional virtual-environment workflow.

The assignments are independent sub-projects, each exploring a core topic in introductory computer graphics.

---

## Repository Structure

```bash
assignment1/
assignment2/
assignment3/
assignment4/
.envrc
README.md       ← (this file)
```

Each assignment folder contains its own codebase, README, and execution entry point.

---

## Using Virtual Environments

Development is intended to happen inside a Python virtual environment.

### With `direnv` (`.envrc` provided)

If you have **direnv** installed:

1. Allow the directory:

   ```bash
   direnv allow
   ```

2. Every time you enter the folder, the virtual environment defined in `.envrc` is activated automatically.

### Manual venv activation (without direnv)

1. Create a venv:

   ```bash
   python -m venv .venv
   ```

2. Activate it:

   **Windows**

   ```bash
   .venv\Scripts\activate
   ```

   **macOS / Linux**

   ```bash
   source .venv/bin/activate
   ```

3. Install shared dependencies:

   ```bash
   pip install -r requirements.txt
   ```

Each assignment can also include its own `requirements.txt` if needed.

---

## Assignment Overview

### **1. Line Drawing Algorithms Exploration**

A study of pixel-based rasterization of lines on a discrete grid.
Includes implementations such as:

* Slope–intercept method
* DDA (Digital Differential Analyzer)
* Bresenham’s line algorithm
  The project provides an interactive UI to visualize output differences between algorithms, pixel-by-pixel.

---

### **2. Transformations Exploration**

An interactive system for exploring 2D geometric transformations using **3×3 homogeneous coordinate matrices**.
Users can apply:

* Translation
* Rotation
* Scaling
* Shearing
* Reflections (including arbitrary line reflections)
  The application visualizes transformations applied cumulatively to a base geometric shape, separated cleanly from rendering logic.

---

### **3. Fractals (Mandelbrot, Julia, IFS)**

A collection of fractal generation experiments:

* **Mandelbrot set** visualization
* **Julia sets** with adjustable parameters
* **Iterated Function Systems (IFS)** including classical fractals like the Fern and Sierpinski triangle
  The project highlights iterative vs. recursive rendering approaches and complex-number dynamics.

---

### **4. L-Systems (Lindenmayer Systems)**

An implementation of deterministic and stochastic **L-systems**.
Includes:

* String-rewriting engine
* Turtle-graphics interpreter
* Tools to explore plant-like structures and procedural patterns
  Students can design grammars and observe structural growth through iterations.

---

## Development Notes

* All assignments are written entirely in **Python**.
* Virtual environments are recommended (either manually or via `direnv`).
* Each assignment includes its own UI or rendering script to run directly with:

```bash
python main.py
```

(or equivalent inside each sub-project).
