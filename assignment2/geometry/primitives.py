import numpy as np


class Point:
    """Immutable logical coordinate point."""
    def __init__(self, x: int, y: int):
        self.coords = np.array([x, y], dtype=int)

    @property
    def x(self): return int(self.coords[0])
    @property
    def y(self): return int(self.coords[1])
    def __repr__(self): return f"Point({self.x}, {self.y})"


class Line:
    """Rasterized line between two points using Bresenham's algorithm."""
    def __init__(self, start: Point, end: Point):
        self.start_point = start
        self.end_point = end
        self.active_pixels = self._bresenham()

    def _bresenham(self) -> list[Point]:
        x0, y0, x1, y1 = self.start_point.x, self.start_point.y, self.end_point.x, self.end_point.y
        points = []

        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep: x0, y0, x1, y1 = y0, x0, y1, x1
        if x0 > x1: x0, y0, x1, y1 = x1, y1, x0, y0

        dx, dy = x1 - x0, abs(y1 - y0)
        error, ystep = dx / 2, 1 if y0 < y1 else -1
        y = y0

        for x in range(x0, x1 + 1):
            coord = (y, x) if steep else (x, y)
            points.append(Point(*coord))
            error -= dy
            if error < 0:
                y += ystep
                error += dx
        return points


class Trapezoid:
    """Simple trapezoid composed of four corner points and connecting lines."""
    def __init__(self, A: Point, B: Point, C: Point, D: Point):
        self.corners = [A, B, C, D]
        self.lines = [Line(A, B), Line(B, C), Line(C, D), Line(D, A)]

    @property
    def active_pixels(self) -> list[Point]:
        pixels = []
        for line in self.lines:
            pixels.extend(line.active_pixels)
        return pixels
