"""
mandelbrot.py
Generate a Mandelbrot set image and save to out/mandelbrot.png.

Usage:
    python mandelbrot.py
"""

import os
import numpy as np
from PIL import Image

OUT_DIR = "out"
os.makedirs(OUT_DIR, exist_ok=True)


def mandelbrot(width=1200, height=900, xlim=(-2.5, 1.0), ylim=(-1.25, 1.25), max_iter=500):
    """
    Compute Mandelbrot escape-time counts using a vectorized algorithm.

    Returns a 2D float array of 'smooth' iteration values (same shape as image).
    """
    # Create coordinate grid in complex plane
    xs = np.linspace(xlim[0], xlim[1], width, dtype=np.float64)
    ys = np.linspace(ylim[0], ylim[1], height, dtype=np.float64)
    X, Y = np.meshgrid(xs, ys)
    C = X + 1j * Y

    # Initialize z and iteration counts
    Z = np.zeros_like(C, dtype=np.complex128)
    # store the iteration at which each point escaped (0 = not escaped yet)
    escaped_at = np.zeros(C.shape, dtype=np.int32)
    # absolute values for smoothing
    absZ = np.abs(Z)

    # Boolean mask for points still being iterated
    not_escaped = np.ones(C.shape, dtype=bool)

    for k in range(1, max_iter + 1):
        # iterate only the not-yet-escaped entries
        Z[not_escaped] = Z[not_escaped] * Z[not_escaped] + C[not_escaped]
        absZ[not_escaped] = np.abs(Z[not_escaped])

        # find newly escaped points
        newly_escaped = not_escaped & (absZ > 2.0)
        if newly_escaped.any():
            escaped_at[newly_escaped] = k
            not_escaped[newly_escaped] = False

        # early exit if all escaped
        if not not_escaped.any():
            break

    # For points that never escaped (likely in the set), mark them with max_iter+1
    escaped_at[escaped_at == 0] = max_iter + 1

    # Smooth iteration counts for coloring:
    # for points that escaped, compute nu = n + 1 - log(log|z|)/log 2
    # we need the |z| at the escape iteration; for simplicity, use current |Z| where available.
    # Avoid invalid logs by clipping.
    absZ_clip = np.clip(absZ, 1e-12, 1e12)
    # compute the fractional escape index where escaped_at <= max_iter
    escaped_mask = escaped_at <= max_iter
    nu = escaped_at.astype(np.float64)
    # only adjust for those that actually escaped
    nu[escaped_mask] = (
        escaped_at[escaped_mask]
        + 1.0
        - np.log(np.log(absZ_clip[escaped_mask])) / np.log(2)
    )

    # points inside set get value 0 (or a high value); here we set them to 0 for black
    nu[~escaped_mask] = 0.0

    return nu


def normalize_to_image(arr, cmap="hot"):
    """
    Convert the float array `arr` into an RGB image.
    `arr` expected to be non-negative; higher -> brighter/colorful.
    Simple colormap implemented using a normalized palette mapping.
    """
    # normalize to [0,1]
    a = arr.astype(np.float64)
    a_min, a_max = a.min(), a.max()
    if a_max > a_min:
        norm = (a - a_min) / (a_max - a_min)
    else:
        norm = np.zeros_like(a)

    # apply a simple palette: map t in [0,1] to RGB using an HSV-like ramp
    # we'll use an easy matplotlib-free gradient: black -> blue -> cyan -> yellow -> white
    def ramp(t):
        # t: ndarray 0..1
        r = np.minimum(1.5 * t, 1.0)
        g = np.minimum(np.maximum(0.0, 3.0 * (t - 0.25)), 1.0)
        b = np.minimum(np.maximum(0.0, 4.0 * (0.5 - np.abs(t - 0.5))), 1.0)
        return (r, g, b)

    r, g, b = ramp(norm)
    rgb = np.dstack(
        (np.clip((r * 255).astype(np.uint8), 0, 255),
         np.clip((g * 255).astype(np.uint8), 0, 255),
         np.clip((b * 255).astype(np.uint8), 0, 255))
    )
    return Image.fromarray(rgb, mode="RGB")


def save_mandelbrot(path=None, width=1200, height=900, max_iter=500):
    if path is None:
        path = os.path.join(OUT_DIR, "mandelbrot.png")

    print("Computing Mandelbrot set: size", width, "x", height, "max_iter", max_iter)
    arr = mandelbrot(width=width, height=height, max_iter=max_iter)
    img = normalize_to_image(arr)
    img.save(path)
    print("Saved:", path)


if __name__ == "__main__":
    save_mandelbrot(width=1600, height=1200, max_iter=800)
