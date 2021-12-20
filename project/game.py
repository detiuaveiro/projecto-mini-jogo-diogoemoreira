import pygame

from input_handler import *
from player import Player

UPDATE = pygame.event.custom_type()
SCALE = 10
HEIGHT = 40
WIDTH = 80

class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((SCALE * WIDTH, SCALE * HEIGHT)) #create the display for the game
        self.clock = pygame.time.Clock() #start counting for game frames
        self.command = InputHandler()

        self.player = Player(SCALE)
        self.enemies = []
        self.eggs = []
        self.food = []

    def loop(self):
        running = True

        pygame.time.set_timer(UPDATE, 30)

        #Event handler
        while running:

            while True:
                event = pygame.event.poll() #receive an event from the poll of events
                if event.type == pygame.NOEVENT: #no events triggered
                    break
                
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN: #if the player pressed a key
                    if event.key == pygame.K_UP:
                        self.command.handleInput("up")
                    elif event.key == pygame.K_DOWN:
                        self.command.handleInput("down")
                    elif event.key == pygame.K_LEFT:
                        self.command.handleInput("left")
                    elif event.key == pygame.K_RIGHT:
                        self.command.handleInput("right")
                    elif event.key == pygame.K_SPACE:
                        self.command.handleInput("space")
                elif event.type == UPDATE:
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
            '''
            self.player.render(self.display)
            self.enemies.render(self.display)
            self.eggs.render(self.display)
            self.food.render(self.display)
            '''

            pygame.display.flip()

if __name__=="__main__":
    pygame.init()
    g = Game()
    g.loop()

    pygame.quit()