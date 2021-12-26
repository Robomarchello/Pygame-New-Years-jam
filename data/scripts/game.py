import pygame,sys,random as rd,time
from pygame.locals import *
from data.scripts.easings import *

class Cursor():
    def __init__(self,radius):
        self.radius = radius
        self.rect = pygame.Rect(-radius,-radius,radius,radius)

        self.maxRes = 16#px
        self.resEase = easeInOutQuart([self.maxRes,0],[0,0],0.0)
        
        self.pressAnim = False 
        self.pressed = False
    def handle_event(self,event):
        if event.type == MOUSEMOTION:
            self.rect.center = event.pos

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 2:
                if self.pressAnim == False:
                    self.pressAnim = True
                    self.pressed = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1 or event.button == 2:
                self.pressed = False 
    def draw(self,screen):
        if self.pressAnim == True:
            if self.resEase.percent < 1:
                self.resEase.percent += 0.05
            else:
                self.pressAnim = False
        else:
            if self.resEase.percent > 0:
                self.resEase.percent -= 0.05
        if self.resEase.percent < 0:
            self.resEase.percent = 0

        resRadius = self.radius+self.resEase.get_pos()[0]
        pygame.draw.circle(screen,(0,0,0),self.rect.center,resRadius,width=2)
        pygame.draw.line(screen,(0,0,0),[self.rect.center[0],self.rect.center[1]-resRadius],[self.rect.center[0],self.rect.center[1]+resRadius-1],width=2)
        pygame.draw.line(screen,(0,0,0),[self.rect.center[0]-resRadius,self.rect.center[1]],[self.rect.center[0]+resRadius-1,self.rect.center[1]],width=2)


class Target():
    def __init__(self,pos,image):
        self.image = image
        self.rect = self.image.get_rect(center=pos)

        self.speed = 2

    def draw(self,screen):
        self.rect.y += self.speed
        screen.blit(self.image,self.rect.topleft)
    
class moving_target():
    def __init__(self):
        pass

class showing_target():
    def __init__(self,pos1,pos2,duration):
        self.pos1 = pos1
        self.pos2 = pos2
        self.duration = duration
        
        self.image = image

    def draw(self,screen):
        pass
class Target_System():
    def __init__(self,cursor):
        self.score = 0
        self.wave = 0

        self.cursor = cursor

        self.target_1 = pygame.image.load('data/assets/target_1.png').convert()
        self.target_1.set_colorkey((0,0,0))
        self.targets = []
        self.targets.append(Target([rd.randint(0,1024),-128],self.target_1))

        self.appendUpdt = time.time()+1

        self.mp = [0,0]

    def draw(self,screen):
        for target in self.targets:
            target.draw(screen)
            if target.rect.top > 1024:
                self.targets.pop(self.targets.index(target))
                self.targets.append(Target([rd.randint(0,1024),-64],self.target_1))

        if self.appendUpdt < time.time():
            self.targets.append(Target([rd.randint(0,1024),-64],self.target_1))
            self.appendUpdt = time.time()+1
            
    def handle_event(self,event):
        if event.type == MOUSEMOTION:
            self.mp = event.pos

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 2:
                
                for target in self.targets:
                    if target.rect.colliderect(self.cursor):
                        self.targets.pop(self.targets.index(target))
                    
