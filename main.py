import pygame,sys
from pygame.locals import *
from data.scripts.game import Cursor
pygame.init()

SCRSIZE = (1024,768)
screen = pygame.display.set_mode(SCRSIZE)
#pygame.display.set_caption()
#pygame window initialization

clock = pygame.time.Clock()

pygame.mouse.set_visible(False)
curs = Cursor(pygame.image.load('data/assets/cursor_1.png').convert_alpha())
def loop():
    event_handlers = [curs]
    while True:
        screen.fill((255,255,255))

        curs.draw(screen)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            for event_handler in event_handlers:
                event_handler.handle_event(event)
        pygame.display.update()
        clock.tick(0)

if __name__ == '__main__':
    loop()
