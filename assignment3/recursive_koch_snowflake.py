import os
import math
from PIL import Image, ImageDraw

# --------------------------------------------------------
# Ensure /out directory exists
# --------------------------------------------------------
OUT_DIR = "out"
os.makedirs(OUT_DIR, exist_ok=True)


# --------------------------------------------------------
# Utility: subdivide a line segment into Koch 4-segment path
# --------------------------------------------------------
def koch_subdivide(p1, p2):
    """
    Given segment P1→P2, return the four-point sequence:
        P1, A, B, C, P2
    where ABC is the equilateral "bump".
    """
    x1, y1 = p1
    x2, y2 = p2

    dx = x2 - x1
    dy = y2 - y1

    # Points subdividing the segment into thirds
    A = (x1 + dx / 3, y1 + dy / 3)
    B = (x1 + 2 * dx / 3, y1 + 2 * dy / 3)

    # Height of the equilateral triangle
    length = math.sqrt(dx*dx + dy*dy)
    h = (math.sqrt(3) / 6) * length

    # Direction perpendicular to the segment
    nx = -dy / length
    ny = dx / length

    # Bump point C
    C = ((A[0] + B[0]) / 2 + nx * h,
         (A[1] + B[1]) / 2 + ny * h)

    return [p1, A, C, B, p2]


# --------------------------------------------------------
# Recursive function
# --------------------------------------------------------
def koch_recursive(points, depth):
    """
    Expand a list of points representing broken line segments into
    the next Koch iteration.
    """
    if depth == 0:
        return points

    new_points = []
    for i in range(len(points) - 1):
        segment = koch_subdivide(points[i], points[i+1])
        # add all except last to avoid duplication
        new_points.extend(segment[:-1])
    new_points.append(points[-1])

    return koch_recursive(new_points, depth - 1)


# --------------------------------------------------------
# Image generator
# --------------------------------------------------------
def generate_koch_snowflake(depth=4, size=1200):
    """
    Render a Koch snowflake of given recursion depth to /out.
    """
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)

    # Initial triangle (equilateral)
    r = size * 0.38
    cx = size / 2
    cy = size * 0.48

    p1 = (cx, cy - r)
    p2 = (cx - r * math.sin(math.pi / 3), cy + r * math.cos(math.pi / 3))
    p3 = (cx + r * math.sin(math.pi / 3), cy + r * math.cos(math.pi / 3))

    # Process each triangle side
    side1 = koch_recursive([p1, p2], depth)
    side2 = koch_recursive([p2, p3], depth)
    side3 = koch_recursive([p3, p1], depth)

    # Draw final snowflake path
    draw.line(side1, fill="black", width=1)
    draw.line(side2, fill="black", width=1)
    draw.line(side3, fill="black", width=1)

    output_path = os.path.join(OUT_DIR, f"koch_snowflake_depth_{depth}.png")
    img.save(output_path)
    print("Saved:", output_path)


# --------------------------------------------------------
# Entry point
# --------------------------------------------------------
if __name__ == "__main__":
    generate_koch_snowflake(depth=5, size=1600)
