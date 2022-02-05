from transition import Transition
from info import Info

class AtMenuTransition(Transition):
    
    def __init__(self):
        self.keyPixel = [
            ((26, 10), (75, 78, 114)),
            ((65, 10), (75, 78, 114))
        ]
        
        
    def evaluate(self, info: Info):
        
        for kp in self.keyPixel:
            if info.getPixelAt(kp[0]) != kp[1]: 
                return False
        
        return True
        