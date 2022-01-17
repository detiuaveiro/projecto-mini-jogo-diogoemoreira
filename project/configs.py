import pickle
from input_handler import *

class Configurations:
    def __init__(self):
        self._keys = {
            "w": Up,
            "a": Left,
            "d": Right,
            "s": Down,
            "space": Jump
        }
        self.save_configs()
        self._keys = None
        self.read_configs()

    @property
    def keys(self):
        return self._keys
    
    def save_configs(self):
        with open('configurations.dat', 'wb') as f:
            pickle.dump([self._keys], f)
    
    def read_configs(self):
        with open('configurations.dat', 'rb') as f:
            self._keys = pickle.load(f)

Configurations().save_configs()