import pygame,sys,math
from pygame.locals import *
pygame.init()

clock = pygame.time.Clock()

#window properties
SCRSIZE = (1024,768)
scr = pygame.display.set_mode(SCRSIZE)
pygame.display.set_caption('raycasting')

rects = [pygame.Rect(100,100,100,100),pygame.Rect(300,400,100,100)]

angle = 0

class ray():
    def __init__(self,startPos,angle,rLen):
        self.startPos = startPos
        self.endPos = startPos

        self.angle = angle
        self.rLen = rLen

        
    def draw(self,surface,rects):
        addX = math.sin(math.radians(self.angle))
        addY = math.cos(math.radians(self.angle))

        self.endPos = [self.startPos[0],self.startPos[1]]

        collide = False
        for bim in range(self.rLen):
            self.endPos[0] += addX
            self.endPos[1] += addY

            for rect in rects:
                if rect.collidepoint(self.endPos):
                    collide = True
            if collide == True:
                break

class raycast():
    def __init__(self,rects):
        self.rects = rects

        self.rays = []

        for Ray in range(37):
            rays.append(ray((300,300),10*Ray,300))

def get_points(rect):
    points = [rect.topleft,rect.topright,rect.bottomleft,rect.bottomright]
    return points

#pygame.mouse.set_visible(False)
while True:
    clock.tick(0)
    scr.fill((0,0,0))

    for rect in rects:
        pygame.draw.rect(scr,(255,255,255),rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                
                pygame.quit()
                sys.exit()

    pygame.display.update()

