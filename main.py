import pygame, logging
from constants.Materials import *
from constants.Constants import *
from pygame.locals import QUIT
from objects.GraphObjects import GridLines, Node
from stuff.FrameTimer import FrameTimers, FrameTimer
from stuff.Input import process_events



pygame.init()


fpsClock = pygame.time.Clock()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Physics Sim...')

# gets added to objects by constructor, so persists
GridLines(PARTICLE_WIDTH, PARTICLE_HEIGHT, 1)

for x in range(10, 100):
    for y in range(10, 100):
        Node(x, y, material=BRICK)
END = FrameTimer(100)
# The main function that controls the game
def main():
    running = True

    # The main game loop
    while running:
        # Get inputs
        process_events()
        # print(len(OBJECTS))

        for pos, obj in list(OBJECTS.items()): # static list, doesn't change on pixel move
            obj.apply_physics(pos, fpsClock.get_time())

        # Render all objects to the screen
        for pos, obj in sorted(OBJECTS.items(), key=lambda x:x[1].z):
            obj.render(WINDOW, pos)

        pygame.display.update()
        [frame_timer.tick() for frame_timer in FrameTimers]
        fpsClock.tick(FPS)
        WINDOW.fill(BACKGROUND)

        # if END.done():
        #     pygame.event.post(pygame.Event(QUIT))

if __name__ == '__main__':
    main()
