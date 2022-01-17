import pygame

class Floor:
    def __init__(self, scale, x=0, y=0):
        self.x, self.y = x,y
        self.sprite = None
        self.scale = scale

    def render(self, display):
        pygame.draw.rect(display, "brown", (self.scale*self.x, self.scale*self.y, self.scale, self.scale))
    
    def clone(self, x=0, y=0):
        return Floor(self.scale, x, y)