import pygame

class Egg:
    '''
    A class that uses flyweight to generate eggs around the map

    Attributes
    ---
    scale
        the scale of the object
    ---

    Methods
    ---
    render(self, display, x,y)
        Draws an image of the object on the display with a position of (x,y)
    ---
    '''
    def __init__(self, scale):
        self.scale = scale

    def render(self, display, x, y):
        pygame.draw.rect(display, 	(255,215,0), (self.scale*x, self.scale*y, self.scale, self.scale))