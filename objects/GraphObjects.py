import pygame, random, logging
from constants.Constants import *
from constants.Materials import SAND
from objects.Position import Pos, is_in_bounds, swap, positions_in_line
from objects.Properties import Material
from abc import abstractmethod, ABCMeta

logger = logging.getLogger(__name__)

def next_smallest_multiple(val: int, mult: int) -> int:
    if val%mult==0:
        return val
    return val - val % mult




class BaseNode(metaclass=ABCMeta):
    def __init__(self):
        self.z = 0
        self.tick_per_frame = 1

    @abstractmethod
    def render(self, window: pygame.Surface, pos: Pos):
        raise NotImplementedError()

    @abstractmethod
    def apply_physics(self, pos: Pos,  delta: int):
        raise NotImplementedError()


class Node(BaseNode):
    def __init__(self, x, y, **kwargs):
        super().__init__()
        self.z = 1

        OBJECTS[Pos(x,y)] = self
        self.radius = kwargs.get('r') or kwargs.get('radius', 3)
        self.material: Material = kwargs.get("material", SAND)
        assert isinstance(self.material, Material)



    def apply_physics(self, pos: Pos,  delta):
        if not is_in_bounds(pos):
            del OBJECTS[pos]
            return

        if random.random() < self.material.fall_p:
            move = self.material.moves.choose_move(pos)
            swap(pos, pos + move.move)

    def render(self, window: pygame.Surface, pos: Pos):
        render_pos = (pos.x * PARTICLE_WIDTH + GRID_X_OFFSET, pos.y * PARTICLE_HEIGHT + GRID_Y_OFFSET)
        pygame.draw.rect(window, self.material.color, pygame.rect.Rect(*render_pos, PARTICLE_WIDTH, PARTICLE_HEIGHT))


class GridLines(BaseNode):
    def __init__(self, *args, size = None, x_offset = 0, y_offset = 0):
        super().__init__()

        self.z = 99
        self.xOffset = x_offset
        self.yOffset = y_offset

        if size:
            if len(args) == 1:
                self.width = args[0]
            try:
                self.xDist = WINDOW_WIDTH // size[0]
                self.yDist = WINDOW_HEIGHT // size[1]
            except TypeError:
                self.xDist = self.yDist = WINDOW_WIDTH // size


        # Args parsing logic
        self.width = 3
        if len(args) == 0:
            self.xDist = self.yDist = 50
        elif len(args) == 1:
            try:
                [self.xDist, self.yDist] = args[0]
            except TypeError:
                self.xDist = self.yDist = args[0]
        elif len(args) == 2:
            try:
                [self.xDist, self.yDist] = args[0]
                self.width = args[1]
            except TypeError:
                self.xDist = self.yDist = args[0]
                self.width = args[1]
        elif len(args) == 3:
            [self.xDist, self.yDist] = args[:2]
            self.width = args[2]
        else:
            raise ValueError(f"Wrong number of arguments provided: {len(args)} must be 0, 1, or 2.")


        OBJECTS[Pos()] = self

    def render(self, window, pos):
        for xi in range(GRID_WIDTH+1):
            x = GRID_X_OFFSET + PARTICLE_WIDTH * xi
            length = GRID_HEIGHT * PARTICLE_WIDTH
            pygame.draw.aaline(window, BLACK, (x, GRID_Y_OFFSET), (x, length + GRID_Y_OFFSET))

        for yi in range(GRID_HEIGHT+1):
            y = GRID_Y_OFFSET + PARTICLE_HEIGHT * yi
            length = GRID_WIDTH * PARTICLE_HEIGHT
            pygame.draw.aaline(window, BLACK, (GRID_X_OFFSET, y), (length + GRID_X_OFFSET, y))

    def apply_physics(self, pos, delta):
        pass # Grid has no interactions

    def __repr__(self) -> str:
        return f"GridLines({self.xDist}, {self.yDist})"

class Line(BaseNode):
    def __init__(self, _x0, _y0, _x1, _y1):
        super().__init__()

        self.x0 = _x0
        self.y0 = _y0
        self.x1 = _x1
        self.y1 = _y1

        OBJECTS[Pos()] = self

    def apply_physics(self, pos: Pos,  delta: int):
        pass

    def render(self, window: pygame.Surface, pos: Pos):
        x0, y0, x1, y1 = [self.x0, self.y0, self.x1, self.y1]

        points = positions_in_line((x0, y0), (x1, y1))

        for x,y in points:
            pygame.draw.rect(window, BLACK, pygame.Rect(x, y, PARTICLE_WIDTH, PARTICLE_HEIGHT))
