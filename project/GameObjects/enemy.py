from random import randrange
import pygame

from map import Map

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
        self.emuAI = EmuAI(self)
    
    @property
    def direction(self):
        return self.enemy_direction
    
    def update(self):
        #make it patrol certain positions
        self.x += self.enemy_direction[0]
        self.y += self.enemy_direction[1]
        if not self._has_ladder:
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
            if event == "no_ladder":
                self._has_ladder = False

class EmuAI():
    def __init__(self, emu:Emu) -> None:
        self._emu = emu
        self._move_horizontal = 1  # -1: emu is moving left, 1: emu is moving right
        self._move_vertical = 1
        self._ladder = False
        self._r = 0 # used to decide if emu goes up or down the ladder
        self._rand_ladder = 0

    def next_move(self, map:Map):
        ##if emu on ladder see if he climbs it
        if(self._emu._has_ladder):
            self._rand_ladder = randrange(10)
            if(self._rand_ladder>4 and not self._ladder):
                self._rand_ladder = randrange(10)
                self._ladder = True
        elif(self._ladder):
            self._ladder = False
        ##

        ##if on ladder
        if(self._ladder):
            self._climb_ladder(map)
            
        else:    
            if(map.walkable_tiles_dic.get((self._emu.x+self._move_horizontal, self._emu.y+1))):
                self._emu.x += self._move_horizontal
            elif(map.walkable_tiles_dic.get((self._emu.x-self._move_horizontal, self._emu.y+1))):
                self._move_horizontal = -self._move_horizontal
        
    def _climb_ladder(self, map:Map):
        #hit the floor
        if(self._r!=0):
            if(map.floor_dic.get((self._emu.x, self._emu.y+1))):
                self._r=0
                self._ladder = False
                return                
            #emu gets out of ladder and walks to right or left if he has floor
            elif(map.walkable_tiles_dic.get((self._emu.x+self._move_horizontal, self._emu.y+1)) and self._rand_ladder<=5):
                self._emu.x += self._move_horizontal
                self._r=0
                self._ladder = False
                return
            elif(map.walkable_tiles_dic.get((self._emu.x-self._move_horizontal, self._emu.y+1)) and self._rand_ladder<=5):
                self._move_horizontal = -self._move_horizontal
                self._r=0
                self._ladder = False
                return
            else:
                self._emu.y += self._move_vertical
                return

        #emu uses ladders
        if(self._rand_ladder>5):
            self._r=1
            if(map.ladder_dic.get((self._emu.x, self._emu.y+1))):
                self._move_vertical = 1
                self._emu.y += self._move_vertical       
                return 
            elif(map.ladder_dic.get((self._emu.x, self._emu.y-1))):
                self._move_vertical = -1
                self._emu.y += self._move_vertical
                return
        elif(self._rand_ladder<=5):
            self._r=1
            if(map.ladder_dic.get((self._emu.x, self._emu.y-1))):
                self._move_vertical=-1
                self._emu.y += self._move_vertical
                return
            elif(map.ladder_dic.get((self._emu.x, self._emu.y+1))):
                self._move_vertical=1
                self._emu.y += self._move_vertical
        
    def wall_collision(self):
        if(self._ladder):
            self._move_vertical= -self._move_vertical
            