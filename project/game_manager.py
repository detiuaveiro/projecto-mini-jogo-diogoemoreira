from observable import Observable

class GameManager(Observable):
    def __init__(self,scale, floor:dict):
        super().__init__()
        self.scale = scale
        self.floor = floor

    def collide(self, ax,ay , bx,by):
        #confirm collision between a and b
        if ax == bx or ay == by:
            return True
        return False
    
    def floor_collide(self, character):
        if self.floor.get((character.x, character.y+1)):
            self.notify(character, "on_floor")
            return True
        return False
