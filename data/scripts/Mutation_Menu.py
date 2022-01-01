import pygame
from pygame.locals import *
import math
from data.scripts.spriteSheet import spriteSheet

class sinePoint():
    def __init__(self,pos,width,angle,speed):
        self.width = width
        self.pos = pos
        self.angle = angle
        self.speed = speed
        
    def update(self):
        self.angle += self.speed

    def get_pos(self):
        pos = [self.pos[0],self.pos[1]]
        pos[0] += math.cos(math.radians(self.angle))*self.width
        return pos
        
class Wave():
    def __init__(self,rect,angle,maxAng,speed,color:pygame.Color):
        self.rect = rect
        self.angle = angle
        self.pointCount = 72
        self.points = []
        self.posBtwn = self.rect.height/self.pointCount
        self.maxAng = maxAng
        self.angleBtwn = self.maxAng//self.pointCount
        
        self.speed = speed

        self.color = color

        for point in range(self.pointCount):
            self.points.append(sinePoint([self.rect.x,self.rect.y+self.posBtwn*point],self.rect.width,self.angleBtwn*point+self.angle,self.speed))
            
    def draw(self,screen):
        index = 0
        for point in self.points:#
            point.update()
            
            if index+1 < len(self.points):
                pygame.draw.line(screen,self.color,point.get_pos(),self.points[index+1].get_pos(),width=10)
            index += 1
        
class dna:
    def __init__(self,rect,maxAng,speed):
        self.speed = speed
        self.Wav = Wave(rect,0,maxAng,speed,pygame.Color(0,200,0))
        self.Wava = Wave(rect,180,maxAng,speed,pygame.Color(0,150,0))

    def draw(self,screen):
        for index in range(len(self.Wav.points)):
            if index%1.5 == 0: 
                if index < len(self.Wav.points):
                    pygame.draw.line(screen,(0,220,0),self.Wav.points[index].get_pos(),self.Wava.points[index].get_pos(),width = 6)
        self.Wav.draw(screen)
        self.Wava.draw(screen)

class Button():
    def __init__(self,pos,image,func):
        self.rect = pygame.Rect(pos,(128,128))
        self.image = image
        self.imageRect = image.get_rect(center=self.rect.center)

        self.borderColor1 = pygame.Color(0,0,0)
        self.borderColor2 = pygame.Color(255,255,255)
        self.borderAnim = 0.0

        self.color = pygame.Color(0,200,0)
        self.colorlock = pygame.Color(0,130,0)
        self.unlock_anim = 0.0

        self.dependence = None

        self.mp = [0,0]

        self.func = func
        self.pressed = False

        self.decline = False

        self.locked = True
    def draw(self,screen):
        if self.locked == False:
            if self.unlock_anim < 0.98:
                self.unlock_anim += 0.02
                
        pygame.draw.rect(screen,self.colorlock.lerp(self.color,self.unlock_anim),self.rect)
        if self.decline == True:
            pygame.draw.rect(screen,(150,0,0),self.rect)
        pygame.draw.rect(screen,self.borderColor1.lerp(self.borderColor2,self.borderAnim),self.rect,width=3)

        self.lock_check()

        if self.rect.collidepoint(self.mp):
            if self.borderAnim < 0.98:
                self.borderAnim += 0.02
        else:
            if self.borderAnim > 0.02:
                self.borderAnim -= 0.02

        screen.blit(self.image,self.imageRect.topleft)

    def lock_check(self):
        if self.dependence == None:
            self.locked = False
        else:
            if self.dependence.pressed == True:
                self.locked = False
    def handle_event(self,event):
        if event.type == MOUSEBUTTONDOWN and self.locked == False:
            if self.rect.collidepoint(self.mp):
                if event.button == 1 or event.button == 2:
                    self.decline = self.func()
                    self.pressed = True
                    

class Mutation_Menu():
    def __init__(self,cursor,hpBar,comboSys):
        self.surface = pygame.Surface((1024,768))

        self.upgrade_count = 0

        #toChange
        self.cursor = cursor
        self.hpBar = hpBar
        self.comboSys = comboSys
        self.damage = self.cursor.damage

        self.font = pygame.font.Font('data/assets/Roboto.ttf',70)
        self.text = self.font.render('M U T A T I O N S',True,(0,200,0))

        self.dna = dna(pygame.Rect(100,0,70,800),300,1)

        self.mp = [0,0]

        self.btnIcons = spriteSheet(pygame.image.load('data/assets/buttonSheet.png').convert_alpha(),(90,90))
        self.buttons = [
            Button([560, 120],self.btnIcons[0],self.addRadius),
            Button([560, 290],self.btnIcons[4],self.combo2),
            Button([360, 290],self.btnIcons[1],self.addHp),
            Button([760, 290],self.btnIcons[2],self.addDamage),
            Button([560, 460],self.btnIcons[5],self.combo4),
            Button([360, 460],self.btnIcons[1],self.addAnotherHp),
            Button([760, 460],self.btnIcons[3],self.addMoreDamage),
            Button([560, 620],self.btnIcons[6],self.test_func),
            Button([360, 620],self.btnIcons[7],self.combo6),
            ]

        self.buttons[1].dependence = self.buttons[0]
        self.buttons[2].dependence = self.buttons[0]
        self.buttons[3].dependence = self.buttons[0]
        self.buttons[4].dependence = self.buttons[1]
        self.buttons[5].dependence = self.buttons[2]
        self.buttons[6].dependence = self.buttons[3]
        self.buttons[7].dependence = self.buttons[4]
        self.buttons[8].dependence = self.buttons[5]

    def draw(self,screen):
        self.surface.fill((50,50,50))
        self.dna.draw(self.surface)
        self.surface.blit(self.text,(370,20))

        for button in self.buttons:
            button.draw(self.surface)

        screen.blit(self.surface,(0,0))

    def test_func(self):
        print('gae')
    def addRadius(self):
        if self.cursor.radius < 48:
            if self.upgrade_count > 0:
                self.upgrade_count -= 1
                
                self.cursor.radius += 16
                self.cursor.rect = pygame.Rect(-self.cursor.radius,-self.cursor.radius,self.cursor.radius,self.cursor.radius)
        else:
            return True
    def addHp(self):
        if self.hpBar.maxHp < 4:
            if self.upgrade_count > 0:
                self.upgrade_count -= 1
                
                self.hpBar.hp += 1
                self.hpBar.maxHp += 1
        else:
            return True
    def addAnotherHp(self):
        if self.hpBar.maxHp < 5:
            if self.upgrade_count > 0:
                self.upgrade_count -= 1
                
                self.hpBar.hp += 1
                self.hpBar.maxHp += 1
        else:
            return True

    def combo2(self):
        if self.comboSys.multiplier < 2:
            if self.upgrade_count > 0:
                self.upgrade_count -= 1
                self.comboThingy = 2
            
    def combo4(self):
        if self.comboSys.multiplier < 4:
            if self.upgrade_count > 0:
                self.upgrade_count -= 1
                self.comboThingy = 4
            
    def combo6(self):
        if self.comboSys.multiplier < 6:
            if self.upgrade_count > 0:
                self.upgrade_count -= 1
                self.comboThingy = 6
            
    def addDamage(self):
        if self.cursor.damage < 2:
            if self.upgrade_count > 0:
                self.upgrade_count -= 1
                self.cursor.damage += 1
        else:
            return True
    def addMoreDamage(self):
        if self.cursor.damage < 3:
            if self.upgrade_count > 0:
                self.upgrade_count -= 1
                self.cursor.damage += 1
        else:
            return True
    def handle_event(self,event):
        if self.upgrade_count > 0:
            if event.type == MOUSEMOTION:
                self.mp = event.pos
                for button in self.buttons:
                    button.mp = event.pos

            for button in self.buttons:
                button.handle_event(event)
