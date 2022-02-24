import string
from observable import Observable

class GameManager(Observable):
    '''
    Using Singleton and Observer pattern, the latter, to create events for other characters

    Attributes
    ---
    __instance
        Instance of the object

    floor
        Dictionary with position of floor tiles
    
    ladders
        Dictionary with position of ladder tiles
    
    walls
        Dictionary with position of walls
    
    eggs
        Dictionary with position of egg objects
    
    food
        Dictionary with position of food objects
    ---

    Methods
    ---
    getInstance()
        If the object was already created, returns its instance
    
    collide(a, b)
        Confirms if a collided with b and returns True if so
    
    walls_collide(character)
        Confirms if character collided with the walls and returns True if so
    
    floor_collide(character)
        Confirm if character is standing on floor and notify it in both cases (is and is not)

    egg_collide(character)
        Confirm if character collided with an egg and if so notify it and remove the egg from play

    others_collide(character)
        Confirm if the character has a ladder and notify it, 
        and confirm if the character collided with food and if so notify it and remove the food from play
    ---
    '''
    __instance=None

    def __init__(self, floor:dict, ladders:dict, walls:set, eggs:dict, food:dict):
        if GameManager.__instance!=None:
            raise Exception("This class is a singleton and its instance is already created!")
        else:
            super().__init__()
            self.floor = floor
            self.ladders = ladders
            self.walls = walls      
            self.eggs = eggs
            self.food = food

    
    @staticmethod
    def getInstance():
        if GameManager.__instance==None:
            raise Exception("Singleton class was never instantiated!")
        else:
            return GameManager.__instance
        

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
    
    def egg_collide(self, character):
        #check if collided with egg
        if self.eggs.get((character.x, character.y)):
            self.notify(character, "on_egg")
            self.eggs.pop((character.x, character.y))
    
    def others_collide(self, character):
        #notify the character if it is on top of a ladder
        if self.ladders.get((character.x, character.y)) or self.ladders.get((character.x, character.y+1)):
            self.notify(character, "on_ladder")
        else:
            self.notify(character, "no_ladder")
        
        #check if collided with food
        if self.food.get((character.x, character.y)):
            self.notify(character, "on_food")
            self.food.pop((character.x, character.y))

