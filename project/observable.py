from observer import Observer

class Observable:

    def __init__(self):
        self._observers=[]
    
    def add_observer(self, callback:Observer):
        self._observers.append(callback)
    
    def notify(self, entity, event):
        for obs in self._observers:
            obs.on_notify(entity, event)
