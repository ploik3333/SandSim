from constants.Constants import *
from objects.Properties import Material, Move, Moves, MovesSet

# MATERIALS
WATER = Material(
        MovesSet(
            Moves(Move(0, 1)),
            Moves(
                Move(1, 1, p=3),
                Move(-1, 1, p=3),
            ),
            Moves(
                Move(2, 1, p=1), # move over 2 in one move
                Move(-2, 1, p=1),
                Move(1, 0, p=4), # move to side
                Move(-1, 0, p=4)
            ),
    ),
    1,
    .9,
    BLUE
)

BRICK = Material(
    Moves(
        *[Move(0, n, p=1/n) for n in range(1, GRID_HEIGHT)]
    ),
    5,
    1,
    DARK_RED
)

SNAD = SAND =  Material(
            MovesSet(
                Moves(
                    Move(0, 2)
                ),
                Moves(
                    Move(0, 1),
                ),
                Moves(
                    Move(1, 1),
                    Move(-1, 1)
                )
        ),
    3,
    1,
    TAN
)

FIRE = Material(
    Moves(*[
            Move((x, y), 1)
                for x in range(-1, 2)
                for y in range(-1, 2)
        ]),
    3,
    .25,
    RED
)

IRON =  Material(
    Moves(),
    5,
    0,
    LIGHT_GRAY
)