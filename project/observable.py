from observer import Observer

class Observable:
    '''
    Parent class for Observable objects, using observer pattern

    Attributes
    ---
    observers
        list of observers to notify
    ---

    Methods
    ---
    add_observer(callback)
        add callback to the list of observers
    
    notify(entity, event)
        notify all observers of the event happening for the entity
    ---
    '''

    def __init__(self):
        self._observers=[]
    
    def add_observer(self, callback:Observer):
        self._observers.append(callback)
    
    def notify(self, entity, event):
        for obs in self._observers:
            obs.on_notify(entity, event)
