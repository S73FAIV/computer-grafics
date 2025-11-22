import numpy as np
from PIL import Image
import os

OUT_DIR = "out"
os.makedirs(OUT_DIR, exist_ok=True)

def check_contractive(transforms, tol=1.0):
    """
    Check if all affine transformations in an IFS are contractive.
    
    transforms: list of (a,b,c,d,e,f)
    tol: maximum allowed singular value (default 1.0)
    
    Returns True if all are contractive, False otherwise.
    """
    for i, (a, b, c, d, _, _) in enumerate(transforms):
        A = np.array([[a, b],
                      [c, d]])
        # singular values measure maximum stretch
        sigma_max = np.linalg.norm(A, 2)  # 2-norm = largest singular value
        if sigma_max >= tol:
            print(f"Transform {i} is NOT contractive: max singular value = {sigma_max}")
            return False
    return True

def ifs_fractal(
    transformations, probabilities, n_points=500_000, image_size=(1000, 1000)
):
    """
    Generate a 2D IFS fractal using the given affine transformations and probabilities.
    transformations: list of (a,b,c,d,e,f)
    probabilities: list of probabilities (must sum to 1)
    """
    width, height = image_size
    points = np.zeros((n_points, 2), dtype=np.float64)
    x, y = 0.0, 0.0

    cum_probs = np.cumsum(probabilities)
    for i in range(n_points):
        r = np.random.rand()
        for j, p in enumerate(cum_probs):
            if r <= p:
                a, b, c, d, e, f = transformations[j]
                x, y = a * x + b * y + e, c * x + d * y + f
                points[i] = (x, y)
                break

    # normalize to image
    x_vals, y_vals = points[:, 0], points[:, 1]
    x_norm = (
        (x_vals - x_vals.min()) / (x_vals.max() - x_vals.min()) * (width - 1)
    ).astype(int)
    y_norm = (
        (y_vals - y_vals.min()) / (y_vals.max() - y_vals.min()) * (height - 1)
    ).astype(int)

    img = np.zeros((height, width), dtype=np.uint32)
    for xi, yi in zip(x_norm, y_norm):
        img[height - 1 - yi, xi] += 1  # flip y-axis

    # normalize and convert to RGB
    img_norm = np.log1p(img) / np.log1p(img.max())
    rgb = (np.stack([img_norm] * 3, axis=-1) * 255).astype(np.uint8)
    return Image.fromarray(rgb, mode="RGB")


def ifs_probabilities(transformations):
    """
    Given a list of affine transformations [(a,b,c,d,e,f), ...],
    return a list of probabilities proportional to the absolute value of the determinant
    of the linear part [[a,b],[c,d]].
    """
    dets = [abs(a * d - b * c) for (a, b, c, d, _, _) in transformations]
    total = sum(dets)
    if total == 0:
        raise ValueError("All determinants are zero, cannot assign probabilities")
    return [d / total for d in dets]


# Example: Sierpinski triangle
# sierpinski_transforms = [
#     (0.5, 0, 0, 0.5, 0, 0),
#     (0.5, 0, 0, 0.5, 0.5, 0),
#     (0.5, 0, 0, 0.5, 0.25, 0.5),
# ]
# sierpinski_probs = ifs_probabilities(sierpinski_transforms)

transforms = [
    (0.00, 0.00, 0.00, 0.16, 0.0, 0.0),    
    (0.85, 0.04, -0.04, 0.85, 0.0, 1.6),   
    (0.20, -0.26, 0.23, 0.22, 0.0, 1.6),
    (-0.15, 0.28, 0.26, 0.24, 0.0, 0.44)
]

if check_contractive(transforms):
    img = ifs_fractal(transforms, ifs_probabilities(transforms))
    img.save(os.path.join(OUT_DIR, "ifs.png"))
