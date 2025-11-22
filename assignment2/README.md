# Graphics Transformation Tool

This directory contains a minimal interactive transformation environment built with **Python**, **Tkinter**, and a compact MVC-style structure.
The application renders a trapezoid on a pixel-grid canvas and allows interactive transformations using 3×3 homogeneous matrices.

This README explains how to install and run the tool, how the project is structured, and how to use the UI.

---

## 1. Requirements

* Python **3.10+**
* Tkinter (included with standard Python installations on Windows/macOS; on Linux install via system package manager)
* `requirements.txt` in this directory

---

## 2. Setup (recommended: virtual environment)

### **Step 1 — Create and activate a virtual environment**

#### **Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### **macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### **Step 2 — Install dependencies**

```bash
pip install -r requirements.txt
```

Tkinter itself is not installed through pip; it must be provided by the OS.
If missing:

* **Ubuntu/Debian:** `sudo apt install python3-tk`
* **Fedora:** `sudo dnf install python3-tkinter`
* **Arch:** `sudo pacman -S tk`

---

## 3. Running the Application

Inside this project folder:

```bash
python main.py
```

The UI window should open immediately.

If using a venv, ensure it is activated when launching.

---

## 4. Project Structure

```stdout
.
├── geometry
│   ├── primitives.py         # Point, Line, Trapezoid classes and pixel generation
│   └── __init__.py
│
├── gui
│   ├── app.py                # Main Tkinter root and layout
│   ├── pixel_frame.py        # Canvas view that renders pixels
│   ├── sidebar.py            # Controller UI (buttons, spinboxes, color pickers)
│   ├── state.py              # State model holding the figure and transformation matrix
│   └── __init__.py
│
├── main.py                   # Entry point
├── README.md                 # This file
├── recording/Recording.mp4   # Example video demo
└── requirements.txt
```

---

## 5. How to Use the GUI

### **Canvas**

* Displays the original trapezoid after applying the current transformation matrix.
* The figure updates immediately when transformations are applied.

### **Translation**

* Set `dx` and `dy`
* Press the corresponding “Apply” button (depending on where you add it)
* Effect stacks with previous transforms.

### **Rotation**

* Enter angle in degrees
* Optional checkbox for CCW/clockwise
* Apply to multiply the rotation into the matrix

### **Scaling**

* Independent `sx`, `sy`
* Multiplies scaling into the matrix

### **Shear (Skew)**

* Shear x/y using degree angles (converted internally to tangents)
* Also cumulative

### **Reflection**

* Various reflection functions exist (line reflection, x-axis, y-axis, custom lines)
* Reflection matrices multiply directly into the transformation matrix

### **Reset Transform**

* Resets the transformation matrix to identity
* Redraws the untouched original figure

### **Color selectors**

* Choose line color and background color
* Canvas updates immediately

### **Canvas size**

* Allows reconfiguring width, height, and pixel scaling factor

### **Information panel**

* Shows:

  * Original trapezoid corner coordinates
  * The current 3×3 transformation matrix (updated after every change)

---

## 6. Notes for Development

* All transformations are **incremental**: every operation left-multiplies a new matrix into `state.transformation_matrix`.
* The original point set is never mutated: only the view is updated.
* Rendering is strictly view-only logic inside `PixelFrame`.
