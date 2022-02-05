from state import State
from info import Info
from math import pi
import numpy as np

class Dead(State):
    
    
    def __init__(self, name):
        super().__init__(name)
    
    
    def tick(self, info: Info):
        
        self.pressSpaceBar = False
        self.move = False
        
        return self.move, self.movement, self.pressSpaceBar
