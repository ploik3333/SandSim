from __future__ import annotations

from functools import cache

from constants.Constants import *
from typing import Any


class Pos:
    """
    Either holds (x,y) as a position, or (None, None) which acts as a unique point that does not Exist
    """

    def __init__(self, *args: int) -> None:
        self._is_imaginary = False
        if len(args) == 0:
            self.x = self.y = 0
            self._is_imaginary = True
        elif len(args) == 1:
            self.x, self.y = args[0]
        elif len(args) == 2:
            self.x, self.y = args
        else:
            raise ValueError("Wrong number of args: either ((x,y), ) or (x,y)")

    def is_imaginary(self):
        return self._is_imaginary

    def __add__(self, other: Pos):
        return Pos(self.x + other.x, self.y + other.y)

    def __iter__(self):
        yield self.x
        yield self.y

    def __eq__(self, other: object, /) -> bool:
        if self.is_imaginary():
            return False
        if isinstance(other, Pos):
            return self.x == other.x and self.y == other.y
        raise TypeError(f"Cant compare Pos and {type(other).__name__}")

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __getitem__(self, key):
        if key == 0: return self.x
        if key == 1: return self.y
        raise ValueError("Key is not in range 2 of: (x,y)")


    def __str__(self) -> str:
        return str((self.x, self.y))

    def __repr__(self) -> str:
        return f"Pos({self.x}, {self.y})"



class ImaginaryPos(Pos):
    def __init__(self, *args: Any):
        self.x = self.y = None

    def is_imaginary(self):
        return False





def swap(pos1, pos2):
    pos1, pos2 = Pos(pos1), Pos(pos2) # just for back compatability and insurance

    if not pos1 in OBJECTS:
        raise ValueError(f"No object at {pos1}")

    if not pos2 in OBJECTS: # can move directly, no need to swap
        OBJECTS[pos2] = OBJECTS[pos1]
        del OBJECTS[pos1]
    else:
        OBJECTS[pos1], OBJECTS[pos2] = OBJECTS[pos2], OBJECTS[pos1]

def is_in_bounds(pos: Pos):
    if pos.is_imaginary():
        return False
    if pos.y >= GRID_HEIGHT:
        return False
    if pos.x < 0 or pos.x >= GRID_WIDTH:
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
    x0, y0, x1, y1 = [*pt1, *pt2]
    points = set()
    dx = abs(x1 - x0)
    sx = (1 if x0 < x1 else -1)
    dy = -abs(y1 - y0)
    sy = (1 if y0 < y1 else -1)
    error = dx + dy

    while 1:
        points.add(Pos(x0, y0))
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