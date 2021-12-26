import pygame,sys
from pygame.locals import *

pygame.init()

SCRSIZE = (1024,768)
screen = pygame.display.set_mode(SCRSIZE)
#pygame.display.set_caption()
#pygame window initialization

clock = pygame.time.Clock()

def loop():
    event_handlers = []
    while True:
        screen.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            for event_handler in event_handlers:
                event_handler.handle_events()
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    loop()
