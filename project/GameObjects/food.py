import pygame

class Food:
    #use flyweight
    def __init__(self, scale):
        self.sprite = None
        self.scale = scale

    def render(self, display, x, y):
        pygame.draw.rect(display, "green", (self.scale*x, self.scale*y, self.scale, self.scale))
        