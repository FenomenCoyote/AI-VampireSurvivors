from transition import Transition
from info import Info

class InGameTransition(Transition):       
        
    def __init__(self):
        self.keyPixel = [
            ((35, 30), (0, 0, 0)),
            ((60, 30), (0, 0, 0)),
            ((46, 40), (0, 0, 0)),
            ((46, 15), (0, 0, 0))
        ]
        
        
    def evaluate(self, info: Info):
        
        for kp in self.keyPixel:
            if info.getPixelAt(kp[0]) == kp[1]: 
                return True
        
        return False
        
        