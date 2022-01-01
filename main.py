import pygame
from pygame.locals import *
import sys
import json

#my scripts:)
from data.scripts.Mutation_Menu import Mutation_Menu
from data.scripts.game import Cursor,Target_System,Wave_Timer,HealthBar,Combo,GameOver
from data.scripts.parallax import parallax
pygame.init()

SCRSIZE = (1024,768)
screen = pygame.display.set_mode(SCRSIZE)
#pygame.display.set_caption()
#pygame window initialization

clock = pygame.time.Clock()

pygame.mouse.set_visible(False)

def loop():
    combo = Combo([20,50])
    healthbar = HealthBar(pygame.Rect(20,20,125,25),(255,0,0),3)
    #load map
    curs = Cursor(8)
    
    info = json.loads(open('data/assets/parallax/map_1/map.json').read())
    imgs = eval(info['images'])
    for img in imgs:
        img.set_colorkey((0,0,0))
    
    prlx = parallax(imgs,eval(info['poses']),eval(info['percents']))

    mutation_menu = Mutation_Menu(curs,healthbar,combo)

    #wave timer
    wt = Wave_Timer(mutation_menu)
    target_system = Target_System(curs,wt,healthbar,combo)

    gameover = GameOver(healthbar)
    
    
    event_handlers = [curs,target_system,prlx,mutation_menu,gameover]
    while True:
        screen.fill((255,255,255))

        if gameover.gameover == False and gameover.appearEff.percent < 1.0:
            if mutation_menu.upgrade_count > 0:
                mutation_menu
                mutation_menu.draw(screen)
                target_system.clean()
            else:
                prlx.draw(screen)
                
                target_system.draw(screen)
                wt.draw(screen)
                combo.draw(screen)
                healthbar.draw(screen)

        if healthbar.hp <= 0:
            gameover.gameover = True
        if gameover.gameover == True:
            gameover.draw(screen)
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
