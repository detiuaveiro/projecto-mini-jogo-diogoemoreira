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
        
        self.game_manager = GameManager(SCALE, self.floor)

        self.game_manager.add_observer(self.player)

    def loop(self):
        running = True

        pygame.time.set_timer(UPDATE, 45)

        #Event handler
        while running:

            while True:
                event = pygame.event.poll() #receive an event from the poll of events
                if event.type == pygame.NOEVENT: #no events triggered
                    break
                
                if event.type == pygame.QUIT:
                    running = False
                    break

                elif event.type == pygame.KEYDOWN: #if the player pressed a key
                    if event.key == pygame.K_UP:
                        self.player.up()
                    elif event.key == pygame.K_DOWN:
                        self.player.down()
                    elif event.key == pygame.K_LEFT:
                        self.player.left()
                    elif event.key == pygame.K_RIGHT:
                        self.player.right()
                    elif event.key == pygame.K_SPACE:
                        self.player.jump()
                elif event.type == UPDATE:
                    if not self.game_manager.floor_collide(self.player):
                        self.player.update()

                    for enemy in self.enemies:
                        if not self.game_manager.floor_collide(enemy):
                            enemy.update() #update enemies' position
                    '''
                    #Update
                    self.player.update() #update player's position
                    for enemy in self.enemies:
                        enemy.update() #update enemies' position

                    #Collisions
                    self.player.collide(self.enemies)
                    self.player.collide(self.eggs)
                    self.player.collide(self.food)
                    '''
            #Test clock to see if the frame time already passed

            #Render
            self.display.fill("white")
            self.player.render(self.display)
            for enemy in self.enemies:
                enemy.render(self.display)

            for pos in self.floor.keys():
                self.floor.get(pos).render(self.display, pos[0], pos[1])
            '''
            self.player.render(self.display)
            self.enemies.render(self.display)
            self.eggs.render(self.display)
            self.food.render(self.display)
            '''

            pygame.display.flip()

if __name__=="__main__":
    pygame.init()

    floor = Floor(SCALE)

    floor_dic = dict()
    for x in range(1,WIDTH):
        floor_dic[(x,HEIGHT-2)] = floor

    g = Game(floor_dic)
    g.loop()

    pygame.quit()