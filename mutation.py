import pygame,sys,math
from pygame.locals import *

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

        self.color = (0,200,0)

        self.mp = [0,0]

        self.func = func
        self.pressed = False
        
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect)
        pygame.draw.rect(screen,self.borderColor1.lerp(self.borderColor2,self.borderAnim),self.rect,width=3)

        if self.rect.collidepoint(self.mp):
            if self.borderAnim < 0.98:
                self.borderAnim += 0.02
        else:
            if self.borderAnim > 0.02:
                self.borderAnim -= 0.02

        screen.blit(self.image,self.imageRect.topleft)

    def handle_event(self,event):
        if event.type == MOUSEBUTTONDOWN and self.pressed == False:
            if self.rect.collidepoint(self.mp):
                if event.button == 1 or event.button == 2:
                    self.func()
                    self.pressed = True
                    
#(557, 186) -- poses
#(367, 302)
#(561, 310)
#826, 301)
#828, 450)
#590, 444)

class mutation_menu():
    def __init__(self):
        self.surface = pygame.Surface((1024,768))

        self.font = pygame.font.Font('data/assets/Roboto.ttf',70)
        self.text = self.font.render('M U T A T I O N S',True,(0,200,0))

        self.dna = dna(pygame.Rect(100,0,70,800),300,1)

        self.mp = [0,0]


        self.btnIcon = pygame.image.load('data/assets/btnicon.png').convert_alpha()
        self.buttons = [
            Button([560, 190],self.btnIcon,self.test_func),
            Button([560, 360],self.btnIcon,self.test_func),
            Button([360, 360],self.btnIcon,self.test_func),
            Button([760, 360],self.btnIcon,self.test_func),
            #Button([826, 301],self.btnIcon,self.test_func),
            #Button([828, 450],self.btnIcon,self.test_func),
            #Button([590, 444],self.btnIcon,self.test_func)
            ]

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

            if event.type == KEYDOWN:
                print(clock.get_fps())

            for event_handler in event_handlers:
                event_handler.handle_event(event)
        pygame.display.update()
        clock.tick(0)

if __name__ == '__main__':
    loop()
