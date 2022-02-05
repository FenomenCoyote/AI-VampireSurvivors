from screenCapture import ScreenImage
import numpy as np
from math import pi, atan2, cos, sin
from PIL.ImageDraw import ImageDraw

class Info: 
    
    def __init__(self, framesPerSecond = 20, makeVideo = False):
        self.sc = ScreenImage()
        
        # self.view initiated in tick
        self.videoMaxFrames = framesPerSecond * 60 # last 1.0 minute 
        
        self.views = []
        
        self.makeVideo = makeVideo
        
        self.hp = 0
        self.nSectors = 24
        
        self.enemyColor = (252, 0, 249)
        self.enemyRedMinColor = 120
        
        self.expGreenMinColor = 32
        
        self.justCloseRadius = 16 # pixels
        self.justCloseRadiusSquared = self.justCloseRadius * self.justCloseRadius # pixels
        self.tooCloseSectorsSpread = self.nSectors // 8

        self._stablishSectors()
        
  
        
    def _stablishSectors(self):
        
        self.sectors = {}
        self.angleStep = 2 * pi / self.nSectors
        for i in range(self.nSectors + 1):
            self.sectors[i * self.angleStep] = np.empty((0, 2))
        
        self._enemiesInSectors_veryClose = {}
        for i in range(self.nSectors):
            self._enemiesInSectors_veryClose[i * self.angleStep] = 0
        
        self._enemiesInSectors = {}
        self._expInSectors = {}
        for i in range(self.nSectors):
            self._enemiesInSectors[i * self.angleStep] = 0
            self._expInSectors[i * self.angleStep] = 0
        
        midX = self.sc.width // 2
        midY = self.sc.height // 2
        
        auxX = auxY = angle = 0
        
        angles = np.asarray(list(self.sectors.keys()))

        for x in range(self.sc.width):
            for y in range(self.sc.height):
                auxX = x - midX
                auxY = y - midY
                angle = np.arctan2(-auxY, auxX)
                if(angle < 0): 
                    angle += 2 * pi
                    
                angle = self._getClosestAngle(angles, angle)
                self.sectors[angle] = np.append(self.sectors[angle], [(x, y)], axis=0)
        
        self.sectors[0] = np.append(self.sectors[0], self.sectors[2 * pi], axis=0)
        self.sectors.pop(2 * pi)
        
    
    def _getClosestAngle(self, angles, angle):
        return angles[(np.abs(angles - angle)).argmin()]
    
    
    def tick(self):
        self.sc.tick()     
        self.view = self.sc.getView()
        # self.view = self.sc.getExampleView()
        self._calculateHP()
        self._calculateEnemiesSectors()
        
        if self.makeVideo:
            self._continueVideo()
    
    
    def getHP(self):
        return self.hp
    
    
    def getViewsArray(self):
        return self.views
    
    
    def getPixelAt(self, xy):
        return self.view.getpixel(xy)
    
    
    def _continueVideo(self):
        img = self.sc.getViewVideo()
    
        draw = ImageDraw(img)
        wHalf = img.width // 2
        hHalf = img.height // 2
        
        step = self.angleStep / 2
        for i in self.sectors.keys():
            draw.line([(wHalf, hHalf), (wHalf + wHalf * cos(i + step), hHalf + hHalf * sin(i + step))])
        
        hpString = "hp: " + str("{:.0f}".format(self.hp * 100))
        msgW, msgH = draw.textsize(hpString)
        draw.text((wHalf - msgW / 2, img.height - 16), hpString, anchor='ms')
                
        self.views.append(img)
        if(len(self.views) > self.videoMaxFrames):
            self.views.pop(0)
        
        
    def _calculateHP(self):
        hp = 0
        for i in range(44, 49):  # 44, 45, 46, 47, 48 length of hp bar
            if(self.view.getpixel((i, 33)) == (221, 10, 21)):  # colour of hp 
                hp += 1.0
        
        hp /= 5.0
        self.hp = hp
                
    
    def _calculateEnemiesSectors(self):
        
        for sector in self._enemiesInSectors_veryClose.keys():
            self._enemiesInSectors_veryClose[sector] = 0
        
        playerPos = (self.sc.width // 2, self.sc.height // 2)
        for sector, pixels in self.sectors.items():
            enemies = 0
            exp = 0
            for pixel in pixels:
                x, y = pixel
                color = self.view.getpixel((x, y))
                if(color[0] >= self.enemyRedMinColor and color[2] > 32):
                    enemies += 1
                    x -= playerPos[0]
                    y -= playerPos[1]
                    if((x * x) + (y * y) < self.justCloseRadiusSquared):
                        for s in range(-self.tooCloseSectorsSpread, self.tooCloseSectorsSpread + 1):
                            self._enemiesInSectors_veryClose[sector + s * self.angleStep] = 1
                elif(color[1] > self.expGreenMinColor):
                    exp += 1
                    
            total = pixels.shape[0]
            self._enemiesInSectors[sector] = enemies / total
            self._expInSectors[sector] = exp / total