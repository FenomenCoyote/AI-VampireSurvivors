from transition import Transition
from info import Info

class GameOverTransition(Transition):
    
    def __init__(self):
        self.keyPixel = [
            ((43, 49), (208, 44, 24)),
            ((46, 49), (208, 44, 24)),
            ((49, 50), (208, 44, 24)),
        ]       
        
    def evaluate(self, info: Info):
        
        for kp in self.keyPixel:
            if info.getPixelAt(kp[0]) != kp[1]: 
                return False
            
        return True
        