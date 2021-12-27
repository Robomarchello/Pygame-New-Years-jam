import pygame
from pygame.locals import *
import sys
import json

#my scripts:)

from data.scripts.game import Cursor,Target_System
from data.scripts.parallax import parallax
pygame.init()

SCRSIZE = (1024,768)
screen = pygame.display.set_mode(SCRSIZE)
#pygame.display.set_caption()
#pygame window initialization

clock = pygame.time.Clock()

pygame.mouse.set_visible(False)
curs = Cursor(17)
target_system = Target_System(curs)
def loop():
    
    info = json.loads(open('data/assets/parallax/map_1/map.json').read())
    imgs = eval(info['images'])
    for img in imgs:
        img.set_colorkey((0,0,0))

    prlx = parallax(imgs,eval(info['poses']),eval(info['percents']))

    event_handlers = [curs,target_system,prlx]
    while True:
        screen.fill((255,255,255))

        prlx.draw(screen)
        
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
