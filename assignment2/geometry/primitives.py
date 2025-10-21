import numpy as np


class Point:
    coords: np.ndarray  # we store the coordinates as numpy array

    def __init__(self, x: int, y: int):
        self.coords = np.array([x, y], dtype=int)

    @property
    def x(self) -> int:
        return self.coords[0]

    @property
    def y(self) -> int:
        return self.coords[1]

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Line:
    start_point: Point
    end_point: Point
    active_pixels: list[Point]

    def __init__(
        self, start_point: Point = Point(0, 0), end_point: Point = Point(0, 0)
    ):
        self.start_point = start_point
        self.end_point = end_point
        self.draw()

    def __str__(self):
        return f"({self.start_point},{self.end_point})"

    def __repr__(self):
        return f"Line({self.start_point}, {self.end_point})"

    def draw(self) -> None:
        pixels = self.get_pixels_with_bresenham(self.start_point, self.end_point)
        self.active_pixels = list(map(lambda point: Point(point[0], point[1]), pixels))
    
    def get_straight_horizontal(self, start_point: Point, end_point: Point) -> np.ndarray:
        x0, y0 = start_point.x, start_point.y
        x1, y1 = end_point.x, end_point.y

        # xs = range with all steps from lower to higher x (ends inclusive)
        xs = np.arange(min(x0, x1), max(x0, x1) + 1)
        # full array, size like xs, bu all values are y0 -> horizontal line
        ys = np.full_like(xs, y0)
        return np.column_stack((xs, ys))


    def get_straight_vertical(self, start_point: Point, end_point: Point) -> np.ndarray:
        x0, y0 = start_point.x, start_point.y
        x1, y1 = end_point.x, end_point.y

        # ys = range with all steps from the lower to the higher y (inclusive)
        ys = np.arange(min(y0, y1), max(y0, y1) + 1)
        # full array, size like ys, but all values x0 -> vertial line!
        xs = np.full_like(ys, x0)
        return np.column_stack((xs, ys))


    def get_perfect_diagonal(self, start_point: Point, end_point: Point) -> np.ndarray:
        x0, y0 = start_point.x, start_point.y
        x1, y1 = end_point.x, end_point.y

        dx = x1 - x0
        dy = y1 - y0

        # get all integer values between start and stop
        xs = np.linspace(start=x0, stop=x1, num=abs(dx) + 1, dtype=int)
        ys = np.linspace(start=y0, stop=y1, num=abs(dy) + 1, dtype=int)
        return np.column_stack((xs, ys))


    def get_pixels_with_bresenham(self, start_point: Point, end_point: Point) -> np.ndarray:
        x0, y0 = start_point.x, start_point.y
        x1, y1 = end_point.x, end_point.y

        # Horizontal line
        if x0 == x1:
            return self.get_straight_horizontal(start_point, end_point)
            # Vertical line
        if y0 == y1:
            return self.get_straight_vertical(start_point, end_point)
        # Perfect diagonal
        if abs(y1 - y0) == abs(x1 - x0):
            return self.get_perfect_diagonal(start_point, end_point)

        # Swap x & y (transpose) if steep:
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0, x1, y1 = y0, x0, y1, x1

        # Swap start & end to always iterate from left to right (x0 <= x1)
        if x0 > x1:
            x0, y0, x1, y1 = x1, y1, x0, y0

        dx = x1 - x0
        dy = abs(y1 - y0)

        # Decision variable
        D = 2 * dy - dx
        y = y0
        ystep = 1 if y0 < y1 else -1

        points = []
        for x in range(x0, x1 + 1):
            if steep:
                px = (y, x)  # transpose back on storing
            else:
                px = (x, y)
            points.append(px)

            if D > 0:
                y += ystep
                D -= 2 * dx

            D += 2 * dy

        return np.array(points, dtype=int)


class Trapezoid:

    corners: list[Point]
    # TODO: decide on representation -> Points or lines?!

    # The points are connected by the lines:
    lines: list[Line]

    def __init__(self, A: Point, B: Point, C: Point, D: Point) -> None:
        self.corners = [A, B, C, D]
        self.lines = []
        self.lines.append(Line(A, B))
        self.lines.append(Line(B, C))
        self.lines.append(Line(C, D))
        self.lines.append(Line(D, A))

    @property
    def A(self) -> Point:
        return self.corners[0]

    @property
    def B(self) -> Point:
        return self.corners[1]

    @property
    def C(self) -> Point:
        return self.corners[2]

    @property
    def D(self) -> Point:
        return self.corners[3]

    
    @property
    def active_pixels(self) -> list[Point]:
        active_pixels = []
        for line in self.lines:
            line.draw()
            active_pixels.extend(line.active_pixels)
        print(self.lines)
        return active_pixels
