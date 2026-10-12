import random, logging
from constants.Constants import OBJECTS
from objects.Position import is_in_bounds, positions_in_line
from objects.Position import add_pos

logger = logging.getLogger(__name__)


class Material:
    def __init__(self, moves_set, _density=3, fall_p=1., color: tuple = (128, 128, 64)):
        self.density = _density
        self.fall_p = fall_p

        self.moves = []
        self.probabilities = []

        for moves in moves_set:
            self.moves.append([])
            self.probabilities.append([])
            for move, p in moves:
                self.moves[-1].append(move)
                self.probabilities[-1].append(p)

        self.color = color

    def choose_move(self, pos):
        for (moves, probs) in zip(self.moves, self.probabilities):
            assert len(moves) == len(probs)
            if any_valid_move(moves, pos, self.density):
                return choose_move(moves, pos, probs, self.density)
        # logger.warning(f"Defaulted on move at {pos} when choosing a move")
        return (0, 0)

    def __str__(self) -> str:
        return f"Material({type(self.moves)}, {self.density}, {self.fall_p}, {self.color})"


def move_is_valid(move, pos, density: int):
    """
    :param move: a move - list of (x,y)
    :type move: tuple[int, int]
    :param density: density of the particle that is moving, if not passed, gets density from OBJECTS[pos]
    :param pos: Absolute location
    :return: If there are any other points in the path of the move
    """
    assert len(move) == 2
    assert len(pos) == 2

    if not is_in_bounds(add_pos(pos, move)):
        return False  # skip expensive calculation if out of bounds

    if not pos in OBJECTS:
        logger.warning("No object at tested position:", pos)


    return valid_in_line(pos, add_pos(pos, move), density)



def any_valid_move(moves, pos, density):
    return any(move_is_valid(move, pos, density=density) for move in moves)


def choose_move(moves, pos, probabilities, density):
    """
    :param moves: list of positions, in the form [(x,y), (x2, y2), ...]
    :type moves: tuple[tuple[int, int]]
    :param pos: position of the object, in the form (x, y)
    :type pos: tuple[int, int]
    :param probabilities: probabilities[i] = p(moves[i])
    :type probabilities: list[float]
    :param density: higher density objects sink through lower density ones
    :type density: int
    :return:
    """
    probabilities = probabilities[:]

    while True:
        if sum(probabilities) <= 0:
            # logger.warning(f"Defaulted on move at {pos} because p=0 / no valid move")
            return (0, 0)
        move = random.choices([*range(len(moves))], probabilities, k=1)[0]
        if move_is_valid(moves[move], pos, density):
            return moves[move]
        else:
            probabilities[move] = 0


def valid_in_line(pt1, pt2, density):
    assert len(pt1) == len(pt2) == 2

    #optimize for cardinal lines
    if pt1[0] == pt2[0]:  # vertical
        dy = int(abs(pt2[1] - pt1[1]) / (pt2[1] - pt1[1]) * 1.3)
        for y in range(pt2[1], pt1[1], -dy):
            pt = (pt1[0], y)
            if pt in OBJECTS and OBJECTS[pt].material.density >= density:
                return False

        return True

    if pt1[1] == pt2[1]:  # horizontal
        dx = int(abs(pt2[0] - pt1[0]) / (pt2[0] - pt1[0]) * 1.3)
        for x in range(pt2[0], pt1[0], -dx):
            pt = (x, pt1[1])
            if pt in OBJECTS and OBJECTS[pt].material.density >= density:
                return False
        return True

    x0, y0, x1, y1 = [*pt1, *pt2]
    dx = abs(x1 - x0)
    sx = (1 if x0 < x1 else -1)
    dy = -abs(y1 - y0)
    sy = (1 if y0 < y1 else -1)
    error = dx + dy

    while 1:
        if (x0, y0) in OBJECTS and OBJECTS[(x0, y0)].material.density >= density:
            if not ((x0, y0) == pt1 or (x0, y0) == pt2):
                return False
        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1:
                return (x0, y0) not in OBJECTS or OBJECTS[(x0, y0)].material.density < density
            error = error + dy
            x0 = x0 + sx

        if e2 <= dx:
            if y0 == y1:
                return (x0, y0) not in OBJECTS or OBJECTS[(x0, y0)].material.density < density
            error = error + dx
            y0 = y0 + sy
