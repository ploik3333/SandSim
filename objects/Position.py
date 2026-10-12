from __future__ import annotations
from math import isnan
import cython
from constants.Constants import *
from typing import Any

def swap(pos1, pos2):
    if not pos1 in OBJECTS:
        raise ValueError(f"No object at {pos1}")

    if not pos2 in OBJECTS: # can move directly, no need to swap
        OBJECTS[pos2] = OBJECTS[pos1]
        del OBJECTS[pos1]
    else:
        OBJECTS[pos1], OBJECTS[pos2] = OBJECTS[pos2], OBJECTS[pos1]

def is_in_bounds(pos):
    if isnan(pos[0]):
        return False
    if pos[1] >= GRID_HEIGHT:
        return False
    if pos[0] < 0 or pos[0] >= GRID_WIDTH:
        return False
    return True

def pos_to_grid(x,y):
    return (x - GRID_X_OFFSET) // PARTICLE_WIDTH, (y - GRID_Y_OFFSET) // PARTICLE_HEIGHT

def grid_to_pos(x, y):
    return x * PARTICLE_WIDTH + GRID_X_OFFSET, y * PARTICLE_HEIGHT + GRID_Y_OFFSET

def pos_of_pixel(x, y):
    return grid_to_pos(*pos_to_grid(x, y))

# @cache
def positions_in_line(pt1, pt2):
    """
    :param pt1: grid Pos for start of the line
    :param pt2: grid Pos for end of the line
    :return: tuple of grid squares passed through by line
    :rtype: tuple[Pos]
    """
    assert len(pt1) == len(pt2) == 2
    x0, y0, x1, y1 = [*pt1, *pt2]
    points = set()
    dx = abs(x1 - x0)
    sx = (1 if x0 < x1 else -1)
    dy = -abs(y1 - y0)
    sy = (1 if y0 < y1 else -1)
    error = dx + dy

    while 1:
        points.add((x0, y0))
        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1: break
            error = error + dy
            x0 = x0 + sx

        if e2 <= dx:
            if y0 == y1: break
            error = error + dx
            y0 = y0 + sy
    return points

def add_pos(a,b):
    assert len(a) == len(b) == 2
    return a[0]+b[0], a[1]+b[1]

def Imaginary_Pos():
    return float('nan'), float('nan')


