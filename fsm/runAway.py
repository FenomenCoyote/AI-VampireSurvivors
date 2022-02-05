from state import State
from info import Info
from math import pi
import numpy as np

class RunAway(State):
    
    
    def __init__(self, name):
        super().__init__(name)
        self.tooManyEnemies = 0.25    
        
    
    def tick(self, info: Info):

        self.move = True
        
        leastEnemies = 1
        zeroEnemiesDir = -1
        bestDir = -1
        
        bestDirs = {}
        noOtherWay = []
        for sector, enemies in info._enemiesInSectors.items():
            if enemies < leastEnemies:
                leastEnemies = enemies
                bestDir = sector
            if enemies < self.tooManyEnemies and info._enemiesInSectors_veryClose[sector] == 0:
                bestDirs[sector] = (info._expInSectors[sector], enemies)

        if len(bestDirs) > 0:
            bestProportion = -1
            for sector, option in bestDirs.items():
                p = option[0] / (option[1] + 1e-6)
                if p > bestProportion:
                    self.movement = sector
                    bestProportion = p
        else:
            self.movement = bestDir
         
        if self.movement < 0:
            self.movement = 0

        return self.move, self.movement, False