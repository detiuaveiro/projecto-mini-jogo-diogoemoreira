from command import Command
from configs import Configurations

class Up(Command):
    #not used for now
    def execute(self, actor):
        actor.up()

class Left(Command):
    def execute(self, actor):
        actor.left()

class Right(Command):
    def execute(self, actor):
        actor.right()

class Down(Command):
    def execute(self, actor):
        actor.down()

class Jump(Command):
    def execute(self, actor):
        actor.down()

class InputHandler:
    def __init__(self):
        conf = Configurations()
        self.command = conf.keys
        for item in self.command.items():
            print(item)

    def handleInput(self, key):
        return self.command[key]
