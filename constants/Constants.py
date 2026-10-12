# Colors
BACKGROUND = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
BLUE = (45, 70, 190)
RED = (255, 58, 91)
DARK_RED = (99, 0, 16)
TAN = (176, 189, 132)
LIGHT_GRAY = (205, 219, 224)

# Constants
FPS = 60
CURSOR_RADIUS = 1
def get_cursor_radius():
    return CURSOR_RADIUS
def set_cursor_radius(v):
    global CURSOR_RADIUS
    CURSOR_RADIUS = v
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800

# Grid definition
PARTICLE_WIDTH = 8
PARTICLE_HEIGHT = 8

GRID_WIDTH = (WINDOW_WIDTH - 200) // PARTICLE_WIDTH
GRID_HEIGHT = WINDOW_HEIGHT // PARTICLE_HEIGHT

GRID_X_OFFSET = 0
GRID_Y_OFFSET = 0


# Define the grid to be accessed everywhere
import asyncio
object_lock = asyncio.Lock()
OBJECTS = {}


