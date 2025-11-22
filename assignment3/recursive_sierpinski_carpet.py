import os
from PIL import Image, ImageDraw

# --------------------------------------------------------
# Ensure /out directory exists
# --------------------------------------------------------
OUT_DIR = "out"
os.makedirs(OUT_DIR, exist_ok=True)


# --------------------------------------------------------
# Recursive Sierpiński Carpet function
# --------------------------------------------------------
def sierpinski_carpet(draw: ImageDraw.Draw, x, y, size, depth):
    """
    Draw a Sierpiński Carpet recursively.

    draw: ImageDraw.Draw
    x, y: top-left corner of current square
    size: side length of current square
    depth: recursion depth
    """
    if depth == 0:
        draw.rectangle([x, y, x + size, y + size], fill="black")
        return

    new = size / 3.0

    # Draw the 8 outer squares (skip the center square)
    for dx in range(3):
        for dy in range(3):
            if dx == 1 and dy == 1:
                # Center square → empty (white)
                continue

            nx = x + dx * new
            ny = y + dy * new
            sierpinski_carpet(draw, nx, ny, new, depth - 1)


# --------------------------------------------------------
# Image generator wrapper
# --------------------------------------------------------
def generate_sierpinski_carpet(depth=4, size=1200):
    """
    Generate a Sierpiński carpet image and store it in /out.
    """
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)

    sierpinski_carpet(draw, 0, 0, size, depth)

    output_path = os.path.join(OUT_DIR, f"sierpinski_carpet_depth_{depth}.png")
    img.save(output_path)
    print("Saved:", output_path)


# --------------------------------------------------------
# Entry point
# --------------------------------------------------------
if __name__ == "__main__":
    generate_sierpinski_carpet(depth=5, size=1200)
