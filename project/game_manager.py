import string
from observable import Observable

class GameManager(Observable):
    def __init__(self,scale, floor:dict, ladders:dict, walls:set):
        super().__init__()
        self.scale = scale
        self.floor = floor
        self.ladders = ladders
        self.walls = walls      

    def collide(self, a , b):
        #confirm collision between a and b
        if a.x == b.x and a.y == b.y:
            return True
        return False
    
    def walls_collide(self, character):
        #confirm if the character has a floor tile beneath him
        #notify the character if it is standing on the floor
        if (character.x, character.y) in self.walls:
            return True
        return False

    def floor_collide(self, character):
        #confirm if the character has a floor tile beneath him
        #notify the character if it is standing on the floor
        if self.floor.get((character.x, character.y+1)):
            self.notify(character, "on_floor")
            return True
        else:
            self.notify(character, "no_floor")
            return False
    
    def on_ladder(self, character):
        #notify the character if it is on top of a ladder
        if self.ladders.get((character.x, character.y)) or self.ladders.get((character.x, character.y+1)):
            self.notify(character, "on_ladder")
        else:
            self.notify(character, "no_ladder")
