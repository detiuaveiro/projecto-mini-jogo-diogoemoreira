from GameObjects.floor import Floor
from GameObjects.ladder import Ladder


class Map:
    """Representation of a Map."""

    def __init__(self, SCALE, filename="level1.txt"):
        self._map = dict()
        self._level = filename

        #generate map
        floor = Floor(SCALE)
        ladder = Ladder(SCALE)

        self.floor_dic = dict()
        self.ladder_dic = dict()

        tiles = {"-": floor,"e": ladder}

        x,y = 0,0

        with open(filename, "r") as f:
            for line in f:
                x=0
                
                for c in line.rstrip():
                    tile = tiles.get(c)
                    if c:
                        print(isinstance(tile, Floor))
                        if isinstance(tile, Floor):
                            self.floor_dic[(x,y)] = floor
                        if isinstance(tile, Ladder):
                            self.ladder_dic[(x,y)] = ladder
                    x+=1
                y+=1