from transition import Transition
from info import Info

class AtMenuTransition(Transition):
    
    def __init__(self):
        self.keyPixel = [
            ((45, 15), (75, 78, 114)),
            ((45, 27), (75, 78, 114)),
            ((45, 35), (75, 78, 114)),
            ((45, 55), (75, 78, 114))
        ]
        
        
    def evaluate(self, info: Info):
        
        for kp in self.keyPixel:
            if info.getPixelAt(kp[0]) != kp[1]: 
                return False
        
        return True