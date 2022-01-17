from observable import Observable

class GameManager(Observable):
    def __init__(self,scale, floor:dict, ladders:dict):
        super().__init__()
        self.scale = scale
        self.floor = floor
        self.ladders = ladders

    def collide(self, ax,ay , bx,by):
        #confirm collision between a and b
        if ax == bx or ay == by:
            return True
        return False
    
    def floor_collide(self, character):
        #confirm if the character has a floor tile beneath him
        #notify the character if it is standing on the floor
        if self.floor.get((character.x, character.y+1)):
            self.notify(character, "on_floor")
            return True
        return False
    
    def on_ladder(self, character):
        #notify the character if it is on top of a ladder
        if self.ladders.get((character.x, character.y)):
            self.notify(character, "on_ladder")
