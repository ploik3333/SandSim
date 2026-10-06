import random, logging
from constants.Constants import OBJECTS
from objects.Position import Pos, is_in_bounds, positions_in_line

logger = logging.getLogger(__name__)

class Move:
    def __init__(self, *args, p: float = 1.):
        if len(args) == 1:
            self.move = Pos(args[0])
        elif len(args) == 2:
            self.move = Pos(args)
        else:
            raise ValueError("The signature of Move is ((x,y), p=1) or (x,y, p=1)")
        self.p = p

    def is_valid_move(self, pos: Pos, density: int | None = None):
        """
        :param density: density of the particle that is moving, if not passed, gets density from OBJECTS[pos]
        :param pos: Absolute location
        :return: If there are any other points in the path of the move
        """
        if not is_in_bounds(pos + self.move):
            return False # skip expensive calculation if out of bounds

        if not pos in OBJECTS:
            logger.warning("No object at tested position:", pos)
            return False

        if density is None:
            density = OBJECTS[pos].material.density

        tiles = positions_in_line(pos, pos + self.move)
        for tile in tiles:
            if tile == pos: continue # skip the tile you are on - it will be occupied
            if tile in OBJECTS and OBJECTS[tile].material.density >= density:
                return False
        return True


    def __iter__(self):
        return iter(self.move)

class Moves:
    def __init__(self, *args: Move):
        self.moves: list[Move] = []
        for arg in args:
            self.add(arg)

    def add(self, move: Move):
        self.moves.append(move)

    def can_move(self, pos) -> bool:
        for move in self.moves:
            if move.is_valid_move(pos):
                return True
        return False


    def choose_move(self, pos) -> Move:
        if not self.can_move(pos):
            return Move((0,0))

        probabilities = [m.p for m in self.moves]

        while True:
            move = random.choices(self.moves, probabilities, k=1)[0]
            if move.is_valid_move(pos):
                return move

    def __iter__(self):
        return iter(self.moves)

class MovesSet:
    def __init__(self, *args: Moves | Move):
        self.moveset = []
        for moves in args:
            self.add(moves)

    def add(self, moves: Moves | Move):
        self.moveset.append(moves)

    def can_move(self, pos) -> bool:
        return any(ms.can_move(pos) for ms in self.moveset)

    def choose_move(self, pos) -> Move:
        for moves in self.moveset:
            if moves.can_move(pos):
                return moves.choose_move(pos)
        return Move((0, 0))

class Material:
    def __init__(self, moves, _density = 3, fall_p = 1., color: tuple = (128, 128, 64)):
        self.density = _density
        self.fall_p = fall_p
        self.moves = moves
        assert type(moves) in [Moves, MovesSet], f"Material moves must Moves or MovesSet, not {type(moves)}"

        self.color = color

    def __str__(self) -> str:
        return f"Material({type(self.moves)}, {self.density}, {self.fall_p}, {self.color})"
