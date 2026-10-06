import pygame, sys, logging
from constants.Materials import *
from pygame.locals import *
from stuff.FrameTimer import FrameTimer
from objects.GraphObjects import Node
from objects.Position import pos_to_grid, Pos

logger = logging.getLogger(__name__)

# main func to be called from main game loop
def process_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    process_mouse_input()



mouse_timeout = FrameTimer(2)
def process_mouse_input():
    pressed = pygame.mouse.get_pressed(5)
    pos = pygame.mouse.get_pos()
    grid_pos = Pos(pos_to_grid(*pos))

    if pressed[1]:
        if grid_pos in OBJECTS:
            del OBJECTS[grid_pos]
    if pressed[3]:
        Node(*grid_pos, material=IRON)

    if mouse_timeout.done():
        if pressed[0]:
            Node(*grid_pos, material=SAND)
        if pressed[2]:
            Node(*grid_pos, material=WATER)
        if pressed[4]:
            Node(*grid_pos, material=BRICK)
        if any([pressed[0], pressed[2], pressed[4]]):
            mouse_timeout.reset()


