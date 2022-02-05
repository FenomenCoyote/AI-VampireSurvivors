from info import Info

class State():
    
    
    def __init__(self, name):
        self._name = name
        self.move = False
        self.movement = 0
        self.pressSpaceBar = False


    def tick(self, info: Info):
        """Hace el update usando el data de info"""
        pass
    
    
    def __str__(self):
        return self._name
    