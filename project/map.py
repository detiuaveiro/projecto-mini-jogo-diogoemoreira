from tkinter import Scale
from GameObjects.egg import Egg
from GameObjects.floor import Floor
from GameObjects.food import Food
from GameObjects.ladder import Ladder


class Map:
    """Representation of a Map."""

    def __init__(self, SCALE, filename="level1.txt"):
        self._map = dict()
        self._level = filename

        #generate map
        floor = Floor(SCALE)
        ladder = Ladder(SCALE)
        egg = Egg(SCALE)
        food = Food(SCALE)

        self.floor_dic = dict()
        self.ladder_dic = dict()
        self.egg_dic = dict()
        self.food_dic = dict()
        self.walkable_tiles_dic = dict()

        tiles = {"-": floor,"e": ladder, "o": egg, "f": food}

        x,y = 0,0

        with open(filename, "r") as f:
            for line in f:
                x=0
                
                for c in line.rstrip():
                    tile = tiles.get(c)
                    if c:
                        if isinstance(tile, Floor):
                            self.floor_dic[(x,y)] = floor
                            self.walkable_tiles_dic[(x,y)] = True
                        elif isinstance(tile, Ladder):
                            self.ladder_dic[(x,y)] = ladder
                            self.walkable_tiles_dic[(x,y)] = True
                        elif isinstance(tile, Egg):
                            self.egg_dic[(x,y)] = egg
                        elif isinstance(tile, Food):
                            self.food_dic[(x,y)] = food
                    x+=1
                y+=1
