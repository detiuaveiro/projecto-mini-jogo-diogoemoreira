import pygame

from player import Player
from enemy import Emu
from game_manager import GameManager
from floor import Floor

UPDATE = pygame.event.custom_type()
SCALE = 10
HEIGHT = 40
WIDTH = 80

class Game:
    def __init__(self, floor_dic:dict):
        self.display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT)) #create the display for the game
        self.clock = pygame.time.Clock() #start counting for game frames
        #self.command = InputHandler()

        self.floor = floor_dic
        self.player = Player(SCALE, HEIGHT, WIDTH)
        self.enemy = Emu(SCALE)
        self.enemies = []
        self.enemies.append(self.enemy.clone(self.enemy.x + 2, self.enemy.y + 1))
        self.eggs = []
        self.food = []
        
        self.game_manager = GameManager(SCALE, self.floor, dict()) #change dict to the ladder dictionary

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
            #confirm if the characters already have floor beneath them
            #if they have, dont update their gravity
            if not self.game_manager.floor_collide(self.player):
                self.player.update() #gravity update

            for enemy in self.enemies:
                if not self.game_manager.floor_collide(enemy):
                    enemy.update() #gravity update

            #Render
            self.display.fill("white")
            self.player.render(self.display)
            for enemy in self.enemies:
                enemy.render(self.display)

            for pos in self.floor.keys():
                self.floor.get(pos).render(self.display, pos[0], pos[1])
            '''
            for egg in self.eggs:
                egg.render(self.display)
            for food in self.food:
                food.render(self.display)
            '''

            pygame.display.flip()

if __name__=="__main__":
    pygame.init()

    floor = Floor(SCALE)

    floor_dic = dict()
    for x in range(1,WIDTH-2):
        floor_dic[(x,HEIGHT-2)] = floor

    g = Game(floor_dic)
    g.loop()

    pygame.quit()