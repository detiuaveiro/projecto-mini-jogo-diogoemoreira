import pygame

class Enemy:
    def __init__(self):
        pass
    
    def clone(self):
        return NotImplemented

class Emu(Enemy):
    #using Prototype pattern
    def __init__(self, scale, x=0, y=0):
        super().__init__()
        self.x, self.y = x, y
        self.sprite = None
        self.enemy_direction = (0, 0)
        self.scale = scale
        self._has_ladder = False
    
    @property
    def direction(self):
        return self.enemy_direction
    
    def update(self):
        #make it patrol certain positions
        self.x += self.enemy_direction[0]
        self.y += self.enemy_direction[1]
        self.y += 1

    def render(self, display):
        pygame.draw.rect(display, "red", (self.scale*self.x, self.scale*self.y, self.scale, self.scale))
    
    def clone(self, x=0, y=0):
        return Emu(self.scale, x, y)
    
    def on_notify(self, entity, event):
        #awaiting certain events
        if entity == self:
            if event == "on_ladder":
                self._has_ladder = True
            else:
                self._has_ladder = False