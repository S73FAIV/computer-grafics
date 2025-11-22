# Assignment 3 — Fractals


This assignment explores several foundational fractal–generation techniques using Python.
Unlike other assignments, this project does **not** provide an interactive UI.
Instead, it consists of a series of standalone scripts that generate fractal images and store them inside an `/out` directory for inspection and comparison.

The four required blocks focus on different mechanisms of fractal formation—recursive subdivision, complex dynamics, escape-time iteration, and probabilistic iterated function systems.

---

## 1. Recursive Fractal Construction

A classical fractal generated purely through **recursion**.
Examples include:

* Sierpinski triangle
* Sierpinski carpet
* Recursive tree structures
* Koch-type subdivisions

The goal is to illustrate how self-similarity arises directly from a subdivision rule applied repeatedly.
The script creates an image in `/out/recursive_fractal.png`.

---

## 2. Julia Set Generation

The Julia set is defined from the iteration:
[
z_{n+1} = z_n^2 + c
]
for a fixed complex number (c).
By exploring different “reasonable” values of (c) (typically in ([-1.5, 1.5] + i[-1.5,1.5])), the script reveals radically different structures ranging from connected filaments to dust-like disconnected sets.

The output includes several Julia sets stored as:
`/out/julia_<c_real>_<c_imag>.png`.

---

## 3. Mandelbrot Set Generation

The Mandelbrot set is defined by the same recurrence as Julia sets, but here:

* (c) varies over the complex plane
* the initial value is always (z_0 = 0)

At each point of the plane, the algorithm iterates the function until the point “escapes” or the maximum iteration count is reached.
The escape-time field is mapped to colors to reveal the full fractal boundary.

The result is stored as:
`/out/mandelbrot.png`.

---

## 4. Iterated Function Systems (IFS) + Chaos Game

An **Iterated Function System** uses a small set of affine transformations—each with an associated probability—to generate a fractal through repeated function application.
Classical examples include:

* Barnsley’s Fern
* Sierpinski triangle (IFS version)
* Fractal trees

This block implements:

1. Deterministic IFS drawing
2. **Chaos Game** sampling, which applies the transformations randomly following their probability distribution

The chaos game typically converges faster and produces expressive, noise-like point clouds.

Outputs include:

* `/out/ifs_deterministic.png`
* `/out/ifs_chaos_game.png`

---

## Output Directory

All generated fractal images are stored under:

```bash
/out
```

This keeps results organized and provides a visual record for report submission or presentation.

---

## Running the Scripts

After activating your virtual environment:

```bash
python recursive_fractal.py
python julia_set.py
python mandelbrot.py
python ifs.py
```

Each script writes its output automatically into `/out`.

---

This assignment provides a compact tour of essential fractal-generation methods and demonstrates how very different mechanisms—recursion, functional iteration, escape dynamics, and probabilistic affine systems—can all produce complex structures from simple rules.
