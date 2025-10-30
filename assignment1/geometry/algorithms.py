import numpy as np
from geometry.primitives import Point

####
# Line Drawing Algorithms
####

## Helper functions:
def get_straight_horizontal(start_point: Point, end_point: Point) -> np.ndarray:
    x0, y0 = start_point.x, start_point.y
    x1, y1 = end_point.x, end_point.y

    #xs = range with all steps from lower to higher x (ends inclusive)
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
    xs = np.linspace(start=x0, stop=x1, num=abs(dx)+1, dtype=int)
    ys = np.linspace(start=y0, stop=y1, num=abs(dy)+1, dtype=int)
    return np.column_stack((xs, ys))


## Algorithm 1: Slope Intercept
def get_pixels_with_slope_intercept(start_point: Point, end_point: Point) -> np.ndarray:
    x0, y0 = start_point.x, start_point.y
    x1, y1 = end_point.x, end_point.y

    dx = x1 - x0
    dy = y1 - y0

    ## vertical line (slope undefined)
    if dx == 0:
        return get_straight_vertical(start_point, end_point)
    ## Horizontal line (dy = 0)
    if dy == 0:
        return get_straight_horizontal(start_point, end_point)
    ## Perfect diagonal line (dy = 0)
    if abs(dx) == abs(dy):
        return get_perfect_diagonal(start_point, end_point)

    # General slope of the line
    m = dy / dx

    # Case abs(m) <= 1 -> step along x axis
    if abs(m) <= 1:
        xs = np.arange(min(x0, x1), max(x0, x1) + 1) # all integer x positions
        ys = m * (xs -x0) + y0 # corresponding y values
        ys = np.round(ys).astype(int) # rasterize to int
        return np.column_stack((xs, ys))
    
    else: # abs(m) > 1 -> step along y axis
        ys = np.arange(min(y0, y1), max(y0, y1) + 1) # all integer y positions
        xs = (ys -y0) / m + x0 # corresponding x values
        xs = np.round(xs).astype(int)
        return np.column_stack((xs, ys))


## Algorithm 2: Digital Diferential Analyzer
def get_pixels_with_dda(start_point: Point, end_point: Point) -> np.ndarray:
    # TODO: skip calculations for vertical, horizontal and perfectly diagonal lines
    # TODO: test functionality in all quadrants of the coord-system

    x0, y0 = start_point.x, start_point.y
    x1, y1 = end_point.x, end_point.y

    dx = x1 - x0
    dy = y1 -y0
    
    # Vertical line
    if dx == 0:
        return get_straight_vertical(start_point, end_point)
    # Horizontal line
    if dy == 0:
        return get_straight_horizontal(start_point, end_point)
    # Perfect diagonal
    if abs(dx) == abs(dy):
        return get_perfect_diagonal(start_point, end_point)

    steps = max(abs(dx), abs(dy))                # number of steps
    t = np.linspace(0, 1, steps + 1)             # parameter between 0..1
    xs = x0 + t * dx                             # interpolate x
    ys = y0 + t * dy                             # interpolate y
    xs = np.round(xs).astype(int)                # rasterize
    ys = np.round(ys).astype(int)
    return np.column_stack((xs, ys))


## Algorithm 3: Bresenham´s line algorithm
def get_pixels_with_bresenham(start_point: Point, end_point: Point) -> np.ndarray:
    x0, y0 = start_point.x, start_point.y
    x1, y1 = end_point.x, end_point.y

    dx = x1 - x0
    dy = y1 -y0
    
    # Vertical line
    if dx == 0:
        return get_straight_vertical(start_point, end_point)
    # Horizontal line
    if dy == 0:
        return get_straight_horizontal(start_point, end_point)
    # Perfect diagonal
    if abs(dx) == abs(dy):
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
    D = 2*dy - dx
    y = y0
    ystep = 1 if y0 < y1 else -1

    points = []
    for x in range(x0, x1 + 1):
        if steep:
            px = (y, x) # transpose back on storing
        else:
            px = (x, y)
        points.append(px)
    
        if D > 0:
            y += ystep
            D -= 2*dx

        D += 2*dy
    
    return np.array(points, dtype=int)



#### Some minor Tests:
# start_point = Point(0,0)
# end_point = Point(10,5)
# print("start_point:", start_point, "\nend_point:", end_point)
# line = get_pixels_with_slope_intercept(start_point, end_point)
# #print("Pixels Slope Intercept:", line)
# line2 = get_pixels_with_dda(start_point, end_point)
# print("Pixels DDA:", line2)
# line3 = get_pixels_with_bresenham(start_point, end_point)
# print("Pixels Bresenham:", line3)
# print(np.array_equal(line, line3))
