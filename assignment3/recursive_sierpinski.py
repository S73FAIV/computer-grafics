import os
from PIL import Image, ImageDraw

# --------------------------------------------------------
# Utility: ensure /out exists
# --------------------------------------------------------
OUT_DIR = "out"
os.makedirs(OUT_DIR, exist_ok=True)


# --------------------------------------------------------
# Recursive Sierpiński routine
# --------------------------------------------------------
def sierpinski(draw: ImageDraw.Draw, depth: int, p1, p2, p3):
    """
    Draw a Sierpiński triangle recursively using three corner points.

    draw: ImageDraw object
    depth: recursion depth (>=0)
    p1, p2, p3: tuples of (x, y)
    """
    if depth == 0:
        draw.polygon([p1, p2, p3], fill="black")
        return

    # Midpoints
    m12 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    m23 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
    m31 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)

    # Recurse on 3 corner triangles
    sierpinski(draw, depth - 1, p1, m12, m31)
    sierpinski(draw, depth - 1, p2, m23, m12)
    sierpinski(draw, depth - 1, p3, m31, m23)


# --------------------------------------------------------
# Image generation
# --------------------------------------------------------
def generate_sierpinski(depth=6, size=1000):
    """
    Render a Sierpiński triangle of a given depth.
    """
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)

    # Corner points of an upright triangle
    p1 = (size / 2, 20)               # Top
    p2 = (20, size - 20)              # Bottom left
    p3 = (size - 20, size - 20)       # Bottom right

    sierpinski(draw, depth, p1, p2, p3)

    output_path = os.path.join(OUT_DIR, f"sierpinski_depth_{depth}.png")
    img.save(output_path)
    print("Saved:", output_path)


# --------------------------------------------------------
# Entry point
# --------------------------------------------------------
if __name__ == "__main__":
    generate_sierpinski(depth=7, size=1200)
