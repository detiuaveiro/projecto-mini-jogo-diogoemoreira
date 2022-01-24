import pygame

class Floor:
    #use flyweight
    def __init__(self, scale):
        self.sprite = None
        self.scale = scale

    def render(self, display, x, y):
        pygame.draw.rect(display, "brown", (self.scale*x, self.scale*y, self.scale, self.scale))