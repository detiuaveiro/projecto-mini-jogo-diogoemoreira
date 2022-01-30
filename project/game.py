import pygame

from GameObjects.enemy import Emu
from GameObjects.player import Player
from GameObjects.floor import Floor
from GameObjects.ladder import Ladder
#from GameObjects.egg import Egg
#from GameObjects.food import Food
from game_manager import GameManager
from map import Map


UPDATE = pygame.event.custom_type()
SCALE = 10
HEIGHT = 40
WIDTH = 80

class Game:
    def __init__(self, walls:dict, floor_dic:dict, ladder_dic:dict):
        self.display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT)) #create the display for the game
        self.clock = pygame.time.Clock() #start counting for game frames      #self.command = InputHandler()

        self.floor = floor_dic
        self.ladder = ladder_dic
        self.player = Player(SCALE, HEIGHT, WIDTH)
        self.enemy = Emu(SCALE)
        self.enemies = []
        self.enemies.append(self.enemy.clone(self.enemy.x + 2, self.enemy.y + 1))
        self.eggs = []
        self.food = []
        
        self.game_manager = GameManager(SCALE, self.floor, self.ladder, walls) #change dict to the ladder dictionary

        self.game_manager.add_observer(self.player)

    def loop(self):
        running = True

        #Event handler
        while running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                elif event.type == pygame.KEYDOWN: #if the player pressed a key
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                
            keys = pygame.key.get_pressed()    
            if keys[pygame.K_UP]:
                self.player.up()
            elif keys[pygame.K_DOWN]:
                self.player.down()
            if keys[pygame.K_LEFT]:
                self.player.left()
            elif keys[pygame.K_RIGHT]:
                self.player.right()

            ## COLLISIONS

            #confirm if the characters already have floor beneath them
            #if they have, dont update their gravity
            self.game_manager.on_ladder(self.player) #confirm if the player has ladders
            if self.game_manager.walls_collide(self.player):
                running=False
            elif not self.game_manager.floor_collide(self.player):
                self.player.update() #gravity update

            for enemy in self.enemies:
                self.game_manager.on_ladder(enemy)
                if not self.game_manager.floor_collide(enemy):
                    enemy.update() #gravity update
                if self.game_manager.collide(self.player, enemy):
                    running=False

            ## RENDER
            self.display.fill("white")
            
            for pos in self.floor.keys():
                self.floor.get(pos).render(self.display, pos[0], pos[1])
            for pos in self.ladder.keys():
                self.ladder.get(pos).render(self.display, pos[0], pos[1])
            
            self.player.render(self.display)
            for enemy in self.enemies:
                enemy.render(self.display)
            '''
            for egg in self.eggs:
                egg.render(self.display)
            for food in self.food:
                food.render(self.display)
            '''

            pygame.display.flip()

if __name__=="__main__":
    pygame.init()

    #generate map
    map = Map(SCALE)
    walls = set()
    #Walls
    for x in range(0,WIDTH):
        walls.add((x,0))
        walls.add((x,HEIGHT))
    for y in range(0,HEIGHT):
        walls.add((0,y))
        walls.add((WIDTH,y))
    #

    g = Game(walls, map.floor_dic, map.ladder_dic)
    g.loop()

    pygame.quit()
