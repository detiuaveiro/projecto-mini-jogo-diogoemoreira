class Spawner:
    '''
    A spawner class used to spawn enemies

    Methods
    ---
    spawn_monster(prototype, x, y)
        Spawns an enemy from its prototype with coordinates x and y
    '''
    def spawn_monster(self, prototype, x, y):
        return prototype.clone(x, y)