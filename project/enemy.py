class Enemy:
    def __init__(self):
        pass
    
    def clone(self):
        return NotImplemented

class Emu(Enemy):
    def __init__(self):
        super().__init__()
        self.x, self.y = 0,0
        self.sprite = None
    
    def clone(self):
        return Emu()