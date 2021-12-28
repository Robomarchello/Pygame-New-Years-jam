import pygame,sys,math
from pygame.locals import *

from data.scripts.spriteSheet import spriteSheet

pygame.init()

SCRSIZE = (1024,768)
screen = pygame.display.set_mode(SCRSIZE)
pygame.display.set_caption('dna animation')

clock = pygame.time.Clock()

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

        self.locked = True
    def draw(self,screen):
        if self.locked == False:
            if self.unlock_anim < 0.98:
                self.unlock_anim += 0.02
                
        pygame.draw.rect(screen,self.colorlock.lerp(self.color,self.unlock_anim),self.rect)
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
                    self.func()
                    self.pressed = True
                    

class mutation_menu():
    def __init__(self):
        self.surface = pygame.Surface((1024,768))

        self.font = pygame.font.Font('data/assets/Roboto.ttf',70)
        self.text = self.font.render('M U T A T I O N S',True,(0,200,0))

        self.dna = dna(pygame.Rect(100,0,70,800),300,1)

        self.mp = [0,0]

        self.btnIcon = pygame.image.load('data/assets/btnicon.png').convert_alpha()

        self.btnIcons = spriteSheet(pygame.image.load('data/assets/buttonSheet.png').convert_alpha(),(90,90))
        self.buttons = [
            Button([560, 190],self.btnIcons[0],self.test_func),
            Button([560, 360],self.btnIcons[5],self.test_func),
            Button([360, 360],self.btnIcons[1],self.test_func),
            Button([760, 360],self.btnIcons[2],self.test_func),
            Button([560, 530],self.btnIcons[4],self.test_func),
            Button([360, 530],self.btnIcons[1],self.test_func),
            Button([760, 530],self.btnIcons[3],self.test_func),
            ]

        self.buttons[1].dependence = self.buttons[0]
        self.buttons[2].dependence = self.buttons[0]
        self.buttons[3].dependence = self.buttons[0]
        self.buttons[4].dependence = self.buttons[1]
        self.buttons[5].dependence = self.buttons[2]
        self.buttons[6].dependence = self.buttons[3]

    def draw(self,screen):
        self.surface.fill((50,50,50))
        self.dna.draw(self.surface)
        self.surface.blit(self.text,(370,20))

        for button in self.buttons:
            button.draw(self.surface)

        screen.blit(self.surface,(0,0))

    def test_func(self):
        print('I love paris')

    def handle_event(self,event):
        if event.type == MOUSEMOTION:
            self.mp = event.pos
            for button in self.buttons:
                button.mp = event.pos

        for button in self.buttons:
            button.handle_event(event)
        
def loop():
    mutat = mutation_menu()
    event_handlers = [mutat]
    while True:
        screen.fill((50,50,50))

        mutat.draw(screen)

        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            for event_handler in event_handlers:
                event_handler.handle_event(event)
        pygame.display.update()
        clock.tick(270)

if __name__ == '__main__':
    loop()
