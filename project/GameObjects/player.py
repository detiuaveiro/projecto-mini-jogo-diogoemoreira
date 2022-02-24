import pygame

from observer import Observer

class Player(Observer):
    '''
    Player class uses singleton pattern and observer to wait for events: 
    standing/not standing on floor/ladder and catching food/egg
    
    Attributes
    ---
    __instance
        Instance of the object
    x
        Horizontal position on the screen
    
    y
        Vertical position on the screen
    
    scale
        Scale used for the screen
    
    _jumping
        Boolean used to know if the object can jump
    
    _jumped
        Boolean used to know if the object is currently jumping
    
    has_ladder
        Boolean used to know if the object is standing on a ladder
    
    score
        Players score
    ---

    Methods
    ---
    getInstance()
        If the object was already created, returns its instance
    
    up()
        If _has_ladder is true decrements y attribute
    down()
        If _has_ladder is true and self._jumping is false Increments y attribute
    left()
        Decrements x attribute
    right()
        Increments x attribute

    jump()
        If not already on a jump and not on a ladder, decreases y by 5 (jumps) and updates _jumped to true 

    update()
        If not on a ladder increments y (gravity)

    render(display)
        Draws an image of the object on the display with a position of (x,y)

    on_notify(entity, event)
        receives events happening to the entity
    ---
    '''
    __instance = None

    def __init__(self, scale, height, width):
        if Player.__instance!=None:
            raise Exception("This class is a singleton and its instance is already created!")
        else:
            super().__init__()
            self.x, self.y = 10, height-10
            self.scale = scale
            self._jumping = True
            self._jumped = False
            self._has_ladder = False
            self.score = 0
            __instance=self
    
    @staticmethod
    def getInstance():
        if Player.__instance==None:
            raise Exception("Singleton class was never instantiated!")
        else:
            return Player.__instance
        
    
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
                self.score+= 50
            
            if event == "on_food":
                self.score+= 30

