import pygame
from GameObjects.egg import Egg

from GameObjects.enemy import Emu
from GameObjects.food import Food
from GameObjects.player import Player
from GameObjects.floor import Floor
from GameObjects.ladder import Ladder
from GameObjects.spawner import Spawner
#from GameObjects.egg import Egg
#from GameObjects.food import Food
from game_manager import GameManager
from map import Map


UPDATE = pygame.event.custom_type()
SCALE = 10
HEIGHT = 40
WIDTH = 80

class Game:
    '''
    A class that handles the game itself, this is where the necessary calls to each game object are made
    '''
    def __init__(self, walls:dict, map:Map):
        self.display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT)) #create the display for the game
        self.clock = pygame.time.Clock() #start counting for game frames      #self.command = InputHandler()
       
        self.font = pygame.font.Font('freesansbold.ttf', 20)

        self.map = map
        self.floor = map.floor_dic
        self.ladder = map.ladder_dic
        self.egg = Egg(SCALE)
        self.food = Food(SCALE)

        self.player = Player(SCALE, HEIGHT, WIDTH)
        enemy = Emu(SCALE)
        
        self.enemies = []
        self.spawner = Spawner()
        self.enemies.append(self.spawner.spawn_monster(enemy, 2, 1))
        
        self.game_manager = GameManager(self.floor, self.ladder, walls, map.egg_dic, map.food_dic) #change dict to the ladder dictionary

        for enemy in self.enemies:
            self.game_manager.add_observer(enemy)
        self.game_manager.add_observer(self.player)

    def loop(self):
        running = True
        time_running=True
        time=300

        #Event handler
        while running:
            self.clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                elif event.type == pygame.KEYDOWN and time_running: #if the player pressed a key
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
            if time_running:
                
                time-= 66.6/1000                    
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
                self.game_manager.others_collide(self.player) #confirm if the player has ladders
                self.game_manager.egg_collide(self.player) #confirm if the player has ladders

                if self.game_manager.walls_collide(self.player):
                    running=False
                elif not self.game_manager.floor_collide(self.player):
                    self.player.update() #gravity update
                
                #enemies
                for enemy in self.enemies:
                    self.game_manager.others_collide(enemy)
                    if self.game_manager.walls_collide(enemy):
                        enemy.emuAI.wall_collision()

                    if self.game_manager.floor_collide(enemy):
                        enemy.update(self.map, False)  
                    else:
                        enemy.update(self.map) #gravity update

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
            for egg in self.game_manager.eggs:
                self.egg.render(self.display, egg[0], egg[1])
            for food in self.game_manager.food:
                self.food.render(self.display, food[0], food[1])

            if not self.game_manager.eggs and time>0:
                time-=1
                self.player.score+=1
                time_running=False
            
            if time<=0:
                time_running=False
            else:
                t_display = self.font.render("Time: " + str(int(time)), True, (0,0,0))
            
            self.display.blit(t_display, (57*SCALE, SCALE))
            
            score = self.font.render("Score: " + str(self.player.score), True, (0,0,0))
            self.display.blit(score, (68*SCALE, SCALE))

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

    g = Game(walls, map)
    g.loop()

    pygame.quit()
