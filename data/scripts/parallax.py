import pygame
from pygame.locals import MOUSEMOTION

class Layer():
    def __init__(self,image,pos,percent):
        self.image = image
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)
        self.percent = percent

    def draw(self,screen,dist):
        posRect = self.rect.copy()
        posRect.x += dist[0]*self.percent
        posRect.y += dist[1]*self.percent

        screen.blit(self.image,posRect.topleft)

class parallax():
    def __init__(self,images,poses,percents):
        self.bg = images[0]
        self.rectBg = self.bg.get_rect()

        self.mp = [0,0]

        self.layerPoses = poses
        self.layerPercents = percents
        self.layerImgs = images
        self.layerImgs.pop(0)
        
        self.layers = []

        for layer in range(len(self.layerPoses)):
            self.layers.append(Layer(self.layerImgs[layer],self.layerPoses[layer],self.layerPercents[layer]))
        self.layers.reverse()
        
    def draw(self,screen):
        dist = [self.mp[0]-self.rectBg.center[0],self.mp[1]-self.rectBg.center[1]]
        screen.blit(self.bg,(0,0))
        for layer in self.layers:
            layer.draw(screen,dist)

    def handle_event(self,event):
        if event.type == MOUSEMOTION:
            self.mp = event.pos
