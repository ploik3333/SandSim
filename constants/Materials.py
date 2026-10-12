from constants.Constants import *
from objects.Properties import Material

# MATERIALS
WATER = Material(
        (
            (
                ((0, 1), 1),
            ),
            (
                ((1, 1), 3),
                ((-1, 1), 3),
            ),
            (
                ((2, 1), 1), # move over 2 in one move
                ((-2, 1), 1),
                ((1, 0), 4), # move to side
                ((-1, 0), 4)
            ),
    ),
    2,
    .9,
    BLUE
)

ALGAE = Material(
        (
            # (
            #     ((0, 1), 1),
            # ),
            (
                ((1, 1), 3),
                ((-1, 1), 3),
            ),
            (
                ((2, 1), 1), # move over 2 in one move
                ((-2, 1), 1),
                ((1, 0), 4), # move to side
                ((-1, 0), 4)
            ),
    ),
    1,
    .9,
    GREEN
)

BRICK = Material(
    (
    [((0, n), 1/n) for n in range(1, GRID_HEIGHT)],
    ),
    5,
    1,
    DARK_RED
)

SNAD = SAND =  Material(
            (
                (
                    (
                        (0, 2), 1
                    ),
                ),
                (
                    (
                        (0, 1), 1
                    ),
                ),
                (
                    (
                        (1, 1), 1
                    ),
                    (
                        (-1, 1), 1
                     ),
                )
        ),
    3,
    1,
    TAN
)

FIRE = Material(
    [
            (((x, y), 1), )
                for x in range(-1, 2)
                for y in range(-1, 2)
        ],
    3,
    .25,
    RED
)

IRON =  Material(
    (),
    5,
    0,
    LIGHT_GRAY
)