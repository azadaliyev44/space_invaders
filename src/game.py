from src.engine.gameScene import GameScene
from src.engine.mainScene import MainScene

class Game:
    def initWindow(self):
        self._window = self._pygame.display.set_mode((self._size["width"], self._size["height"]))
    def __init__(self,width,height,pygame):
        self._pygame = pygame
        self._size = {
            "width":width,"height":height
        }
        # Delta Time
        self.initWindow()
        self._clock = pygame.time.Clock()
        self._FPS = 60
        self._isRunning = [True]
        self._currentScene = MainScene((0,0,0),width,height,pygame,self._isRunning,[self.setScene])
    def setScene(self,name):
        if(name == "MAIN"):
            self._currentScene = MainScene("black",self._size["width"],self._size["height"],self._pygame,self._isRunning,[self.setScene])
        elif (name == "GAME"):
            self._currentScene = GameScene("black",self._size["width"],self._size["height"],self._pygame,self._isRunning,[self.setScene])
    #Core 
    def run(self):
        self._clock.tick(self._FPS)
        while(self._isRunning):
            delta_time = self._clock.tick(self._FPS) / 1000.0
            self._currentScene.update(delta_time)
            self._currentScene.render(self._window)