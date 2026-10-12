import pygame, sys, logging
from constants.Materials import *
from pygame.locals import *
from stuff.FrameTimer import FrameTimer
from objects.GraphObjects import Node
from objects.Position import pos_to_grid

logger = logging.getLogger(__name__)

# main func to be called from main game loop
def process_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    process_mouse_input()
    process_keyboard_inputs()

def set_pos(pos, r=None, material=None):
    if r is None:
        r = get_cursor_radius()
    for x in range(pos[0]-r, pos[0]+r+1):
        for y in range(pos[1] - r, pos[1] + r + 1):
            if material is None:
                if (x, y) in OBJECTS:
                    del OBJECTS[(x, y)]
            else:
                Node(x, y, material=material)

mouse_timeout = FrameTimer(2)
def process_mouse_input():
    pressed = pygame.mouse.get_pressed(5)
    pos = pygame.mouse.get_pos()
    grid_pos = pos_to_grid(*pos)

    if pressed[1]:
        set_pos(grid_pos)
    if pressed[3]:
        set_pos(grid_pos, material=IRON)

    if mouse_timeout.done():
        if pressed[0]:
            set_pos(grid_pos, material=SAND)
        if pressed[2]:
            set_pos(grid_pos, material=WATER)
        if pressed[4]:
            set_pos(grid_pos, material=BRICK)
        if any([pressed[0], pressed[2], pressed[4]]):
            mouse_timeout.reset()

def process_keyboard_inputs():
    keyboard_inputs = pygame.key.get_just_pressed()
    a = [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

    for i, v in enumerate(a):
        if keyboard_inputs[v]:
            set_cursor_radius(i)
            print(get_cursor_radius())

