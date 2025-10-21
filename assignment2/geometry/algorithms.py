import numpy as np
from geometry.primitives import Point

####
# Line Drawing Algorithms
####


## Helper functions:
def get_straight_horizontal(start_point: Point, end_point: Point) -> np.ndarray:
    x0, y0 = start_point.x, start_point.y
    x1, y1 = end_point.x, end_point.y

    # xs = range with all steps from lower to higher x (ends inclusive)
    xs = np.arange(min(x0, x1), max(x0, x1) + 1)
    # full array, size like xs, bu all values are y0 -> horizontal line
    ys = np.full_like(xs, y0)
    return np.column_stack((xs, ys))


def get_straight_vertical(start_point: Point, end_point: Point) -> np.ndarray:
    x0, y0 = start_point.x, start_point.y
    x1, y1 = end_point.x, end_point.y

    # ys = range with all steps from the lower to the higher y (inclusive)
    ys = np.arange(min(y0, y1), max(y0, y1) + 1)
    # full array, size like ys, but all values x0 -> vertial line!
    xs = np.full_like(ys, x0)
    return np.column_stack((xs, ys))


def get_perfect_diagonal(start_point: Point, end_point: Point) -> np.ndarray:
    x0, y0 = start_point.x, start_point.y
    x1, y1 = end_point.x, end_point.y

    dx = x1 - x0
    dy = y1 - y0

    # get all integer values between start and stop
    xs = np.linspace(start=x0, stop=x1, num=abs(dx) + 1, dtype=int)
    ys = np.linspace(start=y0, stop=y1, num=abs(dy) + 1, dtype=int)
    return np.column_stack((xs, ys))


## Algorithm 3: Bresenham´s line algorithm
def get_pixels_with_bresenham(start_point: Point, end_point: Point) -> np.ndarray:
    x0, y0 = start_point.x, start_point.y
    x1, y1 = end_point.x, end_point.y

    # Horizontal line
    if x0 == x1:
        return get_straight_horizontal(start_point, end_point)
        # Vertical line
    if y0 == y1:
        return get_straight_vertical(start_point, end_point)
    # Perfect diagonal
    if abs(y1 - y0) == abs(x1 - x0):
        return get_perfect_diagonal(start_point, end_point)

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
