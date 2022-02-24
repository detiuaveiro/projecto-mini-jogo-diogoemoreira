class Observer:   
    '''
    Parent class for Observer objects, using observer pattern

    Methods
    ---
    on_notify(entity, event)
        entity is notified of the happening of an event
    ---
    ''' 
    def on_notify(self, entity, event):
        raise NotImplemented
