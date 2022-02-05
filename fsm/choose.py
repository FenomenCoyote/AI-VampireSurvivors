from state import State
from info import Info
from math import pi
import numpy as np

class Choose(State):
    
    
    def __init__(self, name):
        super().__init__(name)
        self.itemsPos = [
            (26, 16),
            (26, 28),
            (26, 41),
            (26, 53)
        ]
        
        self.bestItemsSorted = [
            (17, 122, 132), # duplicator
            (23, 161, 99), # fire wand
            (36, 230, 63), # garlic
            (19, 135, 120), # magic wand
            (16, 109, 143), # bible
            (13, 34, 206), # laurel
            (13, 17, 215), # cross
            (15, 0, 240), # vandalier
            (36, 227, 64), # rune tracer
            (15, 0, 237), # axe
            (14, 0, 234), # empty tome
            (16, 116, 137), # spinach
            (24, 164, 97), # spellbinder
            (13, 0, 221), # candelabrador
            (13, 9, 218), # clover
            (20, 141, 114), # whip
            (22, 151, 107), # clock lancet
            (33, 211, 68), # knife
            (15, 0, 240), # peachone
            (15, 0, 240), # ebony wings
            (18, 129, 126), # santa water
            (29, 193, 77), # armor
            (21, 147, 110), # wings
            (32, 208, 69), # bone
            (13, 38, 203), # lighting ring
            (14, 0, 231), # attractorb
            (13, 38, 179), # pentagram
            (13, 83, 166), # hollow heart
            (30, 196, 75), # pummarola
            (35, 224, 64), # bracer
            (18, 125, 129), # crown
        ]
        
        self.queueSteps = []

    
    def tick(self, info: Info):
        
        self.pressSpaceBar = False
        self.move = True
        
        if len(self.queueSteps) == 0:
            bestItem = 100
            itemPos = 0
            it = 0
            for pixel in self.itemsPos:
                if pixel in self.bestItemsSorted:
                    index = self.bestItemsSorted.index(pixel)
                    if index < bestItem: 
                        index = bestItem
                        itemPos = it
                it += 1

            # go up 3 times
            for i in range(3):
                self.queueSteps.append(pi/2)
            # go down x times (0 , 1, 2, or 3 times)
            for i in range(itemPos):
                self.queueSteps.append(3 * pi / 2) 
            
            self.queueSteps.append(0) 
        else:
            self.movement = self.queueSteps[0]
            if self.movement == 0: self.pressSpaceBar = True
            self.queueSteps.pop(0)
        
        return self.move, self.movement, self.pressSpaceBar
