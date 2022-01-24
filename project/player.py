import pygame

from observable import Observable

class Player(Observable):
    def __init__(self, scale, height, width):
        super().__init__()
        self.scale = scale
        self.x, self.y = 10, height-10
        self._jumping = True
        self._has_ladder = False
        self.sprite = None
    
    def up(self):
        #needs to confirm if there is a ladder
        if self._has_ladder:
            self.y -= 1
        
    def down(self):
        #needs to confirm if there is a ladder
        self.y += 1
    def left(self):
        self.x -= 1
    def right(self):
        self.x += 1
    def jump(self):
        if self._jumping:
            self.y -= 5

    def update(self):
        self.y += 1
    
    def render(self, display):
        pygame.draw.rect(display, "blue", (self.scale*self.x, self.scale*self.y, self.scale, self.scale))

    def on_notify(self, entity, event):
        #awaiting certain events
        if entity == self:
            if event == "on_floor":
                #when player on the ground allow jumping again
                self._jumping = True
            else:
                self._jumping = False

            if event == "on_ladder":
                self._has_ladder = True
            else:
                self._has_ladder = False