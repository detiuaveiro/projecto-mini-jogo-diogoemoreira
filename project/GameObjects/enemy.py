from random import randrange
import pygame

from map import Map
from observer import Observer

class Enemy(Observer):
    '''
    A parent class for prototype pattern which inherits from observer

    Methods
    ---
    clone(self, x,y)
        Creates another object by copying this protoype
    ---
    '''
    def __init__(self):
        pass
    
    def clone(self, x=0, y=0):
        return NotImplemented

class Emu(Enemy):
    '''
    Inherits from Enemy class, using pattern prototype and observer to wait for events: 
    eating food and standing on a ladder

    Attributes
    ---
    x
        Horizontal position on the screen
    
    y
        Vertical position on the screen
    
    scale
        Scale used for the screen
    
    has_ladder
        Boolean used to know if the object is standing on a ladder
    
    stop_timer
        Integer used to stop the object when he eats food
    
    emuAI
        Artificial Intelligence used for this object
    ---

    Methods
    ---
    update(map, fall)
        Calls the AI for the next move to udpdate position and if falling also updates its position.
        If the attribute stop_timer is different from 0 does not update its position and instead decrements stop_timer
    
    render(display)
        Draws an image of the object on the display with a position of (x,y)
    
    clone(x, y)
        returns a clone of the object in the position x and y
    
    on_notify(entity, event)
        receives events happening to the entity
    ---
    '''
    def __init__(self, scale, x=0, y=0):
        super().__init__()
        self.x, self.y = x, y
        self.scale = scale
        self._has_ladder = False
        self.stop_timer = 0
        self.emuAI = EmuAI(self)
    
    def update(self, map, fall=True):
        #make it patrol certain positions
        if self.stop_timer==0:
            self.emuAI.next_move(map)
            if fall and not self._has_ladder:
                self.y += 1
        else:
            self.stop_timer-=1

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
            
            if event == "on_food":
                self.stop_timer=15

class EmuAI():
    '''
    Artificial Intelligence for Emu class

    Attributes
    ---
    _emu
        Object for which the AI is calculating the next movement
    
    _move_horizontal
        Integer used to know where the object is moving horizontally, -1: object is moving left, 1: object is moving right
    
    _move_vertical
        Integer used to know where the object is moving vertically, -1: object is moving up, 1: object is moving down
    
    _ladder
        Boolean to decide if the object is on a ladder
    
    _r
        Integer used to decide if the object will go up or down the ladder
    
    _rand_ladder
        Integer for randomizing the objects movements
    ---

    Methods
    ---
    next_move(map)
        Decides the next movement for the object confirming possible moves
    
    climb_ladder(map)
        Decides the move of the object if he is standing on a ladder
    
    wall_collision()
        If the object would collide with a wall he changes his direction
    ---
    '''
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
            