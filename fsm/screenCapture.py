from PIL import Image, ImageGrab

class ScreenImage: 
    
    IMAGE_X1 = 400
    IMAGE_Y1 = 135
    IMAGE_X2 = 1520
    IMAGE_Y2 = 870
    
    def __init__(self, viewScaleFactor = 12, videoScaleFactor = 4):
        self.viewExample = Image.open("example.png")
        
        self.SCALE_FACTOR = 1 / viewScaleFactor
        self.SCALE_FACTOR_VIDEO = 1 / videoScaleFactor
        
        self.width = int((self.IMAGE_X2 - self.IMAGE_X1) * self.SCALE_FACTOR)
        self.height = int((self.IMAGE_Y2 - self.IMAGE_Y1) * self.SCALE_FACTOR)
        
        # self.tick()
        # self.getView().save("example.png")


    def tick(self):
        self.image = ImageGrab.grab(bbox=(self.IMAGE_X1, self.IMAGE_Y1, self.IMAGE_X2, self.IMAGE_Y2))

        
    def getView(self):
        return self.image.resize((int(self.image.size[0] * self.SCALE_FACTOR), int(self.image.size[1] * self.SCALE_FACTOR)), Image.NEAREST, None, None)
        #return self.image.reduce(self.SCALE_FACTOR)
    
    def getViewVideo(self):
        return self.image.resize((int(self.image.size[0] * self.SCALE_FACTOR_VIDEO), int(self.image.size[1] * self.SCALE_FACTOR_VIDEO)), Image.NEAREST, None, None)
        #return self.image.reduce(self.SCALE_FACTOR_VIDEO)

    def getExampleView(self):
        return self.viewExample