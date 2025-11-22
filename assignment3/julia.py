"""
julia.py
Generate a Julia set image and save to out/julia.png.

Usage:
    python julia.py
"""

import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

OUT_DIR = "out"
os.makedirs(OUT_DIR, exist_ok=True)


def julia(width=1200, height=900, xlim=(-1.5, 1.5), ylim=(-1.25, 1.25),
          c=-0.8 + 0.156j, max_iter=500):
    """
    Compute Julia set escape-time counts using a vectorized algorithm.
    Returns a 2D float array of smooth iteration values.
    """
    xs = np.linspace(xlim[0], xlim[1], width, dtype=np.float64)
    ys = np.linspace(ylim[0], ylim[1], height, dtype=np.float64)
    X, Y = np.meshgrid(xs, ys)
    Z = X + 1j * Y

    escaped_at = np.zeros(Z.shape, dtype=np.int32)
    absZ = np.abs(Z)
    not_escaped = np.ones(Z.shape, dtype=bool)

    for k in range(1, max_iter + 1):
        Z[not_escaped] = Z[not_escaped] ** 2 + c
        absZ[not_escaped] = np.abs(Z[not_escaped])

        newly_escaped = not_escaped & (absZ > 2.0)
        if newly_escaped.any():
            escaped_at[newly_escaped] = k
            not_escaped[newly_escaped] = False

        if not not_escaped.any():
            break

    escaped_at[escaped_at == 0] = max_iter + 1

    absZ_clip = np.clip(absZ, 1e-12, 1e12)
    escaped_mask = escaped_at <= max_iter
    nu = escaped_at.astype(np.float64)
    nu[escaped_mask] = (
        escaped_at[escaped_mask]
        + 1.0
        - np.log(np.log(absZ_clip[escaped_mask])) / np.log(2)
    )
    nu[~escaped_mask] = 0.0

    return nu


def normalize_to_image(arr, cmap_name):
    """
    Convert a 2D float array into an RGB image using matplotlib colormap
    with logarithmic scaling for better detail.
    """
    a = arr.astype(np.float64)
    a_min, a_max = a.min(), a.max()
    norm = (a - a_min) / (a_max - a_min) if a_max > a_min else np.zeros_like(a)
    
    # logarithmic scaling
    norm = np.log1p(norm * 10) / np.log1p(10)

    cmap = plt.get_cmap(cmap_name)
    rgb_float = cmap(norm)[..., :3]
    rgb = (rgb_float * 255).astype(np.uint8)
    return Image.fromarray(rgb, mode="RGB")


def save_julia(path=None, width=1600, height=1200, c=-0.81 + 0.156j,
               max_iter=800, cmap_name="plasma"):
    # sanitize c for filename
    c_str = f"{c.real:.3f}_{c.imag:.3f}".replace("-", "m").replace(".", "p")
    filename = f"julia_c{c_str}_{cmap_name}.png"
    if path is None:
        path = os.path.join(OUT_DIR, filename)

    print("Computing Julia set: size", width, "x", height, "max_iter", max_iter, "c =", c)
    arr = julia(width=width, height=height, c=c, max_iter=max_iter)
    img = normalize_to_image(arr, cmap_name=cmap_name)
    img.save(path)
    print("Saved:", path)


if __name__ == "__main__":
    save_julia()
