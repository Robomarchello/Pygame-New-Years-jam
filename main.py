import pygame,sys
from pygame.locals import *
from data.scripts.game import Cursor,Target_System
pygame.init()

SCRSIZE = (1024,768)
screen = pygame.display.set_mode(SCRSIZE)
#pygame.display.set_caption()
#pygame window initialization

clock = pygame.time.Clock()

pygame.mouse.set_visible(False)
curs = Cursor(17)
target_system = Target_System()
def loop():
    event_handlers = [curs]
    while True:
        screen.fill((255,255,255))

        target_system.draw(screen)
        
        curs.draw(screen)
        
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            for event_handler in event_handlers:
                event_handler.handle_event(event)
        pygame.display.update()
        clock.tick(240)

if __name__ == '__main__':
    loop()
