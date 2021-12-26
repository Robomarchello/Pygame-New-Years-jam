import pygame,sys
from pygame.locals import *

class Cursor():
    def __init__(self,image):
        self.image = image
        self.rect = self.image.get_rect()

    def handle_event(self,event):
        if event.type == MOUSEMOTION:
            self.rect.center = event.pos

    def draw(self,screen):
        screen.blit(self.image,self.rect.topleft)
