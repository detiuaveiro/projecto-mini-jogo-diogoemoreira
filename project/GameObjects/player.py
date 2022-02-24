import pygame

from observable import Observable

class Player(Observable):
    def __init__(self, scale, height, width):
        super().__init__()
        self.scale = scale
        self.x, self.y = 10, height-10
        self._jumping = True
        self._jumped = False
        self._has_ladder = False
        self.sprite = None
        self.score = 0
    
    def up(self):
        #needs to confirm if there is a ladder
        if self._has_ladder:
            self.y -= 1
        
    def down(self):
        #needs to confirm if there is a ladder
        if self._has_ladder and not self._jumping:
            self.y += 1
    def left(self):
        self.x -= 1
    def right(self):
        self.x += 1
    def jump(self):
        if self._jumping and not self._has_ladder:
            self._jumped = True
            self.y -= 5

    def update(self):
        if not self._has_ladder:
            if self._jumped:
                self._jumped=False
            else:
                self.y += 1
    
    def render(self, display):
        pygame.draw.rect(display, "blue", (self.scale*self.x, self.scale*self.y, self.scale, self.scale))

    def on_notify(self, entity, event):
        #awaiting certain events
        if entity == self:
            if event == "on_floor":
                #when player on the ground allow jumping again
                self._jumping = True
            if event == "no_floor":
                self._jumping = False

            if event == "on_ladder":
                self._has_ladder = True
            if event == "no_ladder":
                self._has_ladder = False
            
            if event == "on_egg":
                self.score+= 25
            
            if event == "on_food":
                self.score+= 10

