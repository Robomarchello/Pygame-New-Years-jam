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
        self.speedmult = 0.7

    def draw(self,screen):
        self.rect.y += self.speed*self.speedmult
        screen.blit(self.image,self.rect.topleft)
    
class Armored_Target():
    def __init__(self,pos,images):
        self.crntImg = 0
        self.images = images
        self.rect = self.image.get_rect(center=pos)

        self.speed = 2
        self.speedmult = 0.7

    def draw(self,screen):
        self.rect.y += self.speed*self.speedmult
        screen.blit(self.image,self.rect.topleft)

class Showing_Target():
    def __init__(self,pos1,pos2,image,destImg,brick,duration):
        self.pos1 = pos1
        self.pos2 = pos2
        self.ease = easeOutQuart(pos1,pos2,0.0)

        self.duration = time.time()+duration
        self.moveDir = True
        self.fromDir = {'left':False,'right':False}

        self.destroyed = False
        
        if pos1[0] < pos2[0]:
            self.fromDir['left'] = True
        elif pos1[0] > pos2[0]:
            self.fromDir['right'] = True
        #set_pos
        self.brick = brick
        self.brickRect = brick.get_rect()

        self.destImg = destImg
        self.image = image
        self.imgrect = image.get_rect()

        self.speed = 0.5

        self.update_pos()

    def draw(self,screen):
        screen.blit(self.brick,self.brickRect.topleft)
        if self.destroyed == False:
            screen.blit(self.image,self.imgrect.topleft)
        else:
            screen.blit(self.destImg,self.imgrect.topleft) 
        if self.moveDir == True:
            if self.ease.percent < 1:
                self.ease.percent += 0.01*self.speed

        else:
            if self.ease.percent > 0:
                self.ease.percent -= 0.01*self.speed

        if self.duration < time.time():
            self.moveDir = False

        #set_pos
        get_pos = self.ease.get_pos()
        self.brickRect.center = get_pos
        self.brickRect.right = get_pos[0]
        if self.fromDir['left'] == True:
            self.imgrect.center = [self.imgrect.center[0],self.brickRect.center[1]]
            self.imgrect.center = [self.brickRect.right,self.imgrect.center[1]]
        elif self.fromDir['right'] == True:
            self.imgrect.center = [self.imgrect.center[0],self.brickRect.center[1]]
            self.imgrect.center = [self.brickRect.left,self.imgrect.center[1]]
        

    def update_pos(self):
        self.brickRect.center = self.pos1
        self.brickRect.right = self.pos1[0]
        self.imgrect.center = [self.brickRect.right,self.imgrect.center[1]]
        self.imgrect.center = [self.imgrect.center[0],self.brickRect.center[1]]


        
class Target_System():
    def __init__(self,cursor):
        self.score = 0
        self.wave = 0

        self.cursor = cursor

        self.target_1 = pygame.image.load('data/assets/target_1.png').convert()
        self.target_1.set_colorkey((0,0,0))
        self.targets = []
        self.targets.append(Target([rd.randint(0,1024),-128],self.target_1))

        self.brick = pygame.image.load('data/assets/wood_horizontal.png').convert_alpha()
        
        self.showTarget = pygame.image.load('data/assets/target_1_big.png').convert()
        self.showTarget.set_colorkey((0,0,0))
        self.showTargetDestroyed = pygame.image.load('data/assets/target_1_big_destroyed.png').convert()
        self.showTargetDestroyed.set_colorkey((0,0,0))
        
        self.show_targets = []
        self.show_targets_poses = [[[-64,250],[275,250]],[[1088+self.brick.get_width(),250],[1088,250]]]
        #self.show_targets.append(Showing_Target([-64,250],[275,250],self.showTarget,self.brick,1))
        #self.show_targets.append(Showing_Target([1088+self.brick.get_width(),250],[1088,250],self.showTarget,self.brick,1))
        self.appendUpdt = time.time()+1

        self.mp = [0,0]

    def draw(self,screen):
        #Append targets
        if self.appendUpdt < time.time():
            if rd.randint(0,5) == 5:
                pos = rd.choice(self.show_targets_poses)
                ps = rd.randint(100,600)
                pos[0][1] = ps
                pos[1][1] = ps
                self.show_targets.append(Showing_Target(pos[0],pos[1],self.showTarget,self.showTargetDestroyed,self.brick,1))

            self.targets.append(Target([rd.randint(0,1024),-64],self.target_1))
            self.appendUpdt = time.time()+1

        #loop targets
        for target in self.targets:
            target.draw(screen)
            if target.rect.top > 768:
                self.targets.pop(self.targets.index(target))
                #self.targets.append(Target([rd.randint(0,1024),-64],self.target_1))

        for target in self.show_targets:
            target.draw(screen)

            if target.ease.percent <= 0.0:
                self.show_targets.pop(self.show_targets.index(target))
    def handle_event(self,event):
        if event.type == MOUSEMOTION:
            self.mp = event.pos

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1 or event.button == 2:
                
                for target in self.targets:
                    if target.rect.colliderect(self.cursor):
                        self.targets.pop(self.targets.index(target))
                        
                for target in self.show_targets:
                    if target.imgrect.colliderect(self.cursor):
                        target.destroyed = True
