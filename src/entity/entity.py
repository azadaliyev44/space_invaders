import pygame

class Entity:
    def initVariables(self):
        self._movePos = {"x":0,"y":0}
    def initSprite(self):
        self._sprite = pygame.transform.scale(
            pygame.image.load(self._texture), 
            (self._size["width"], self._size["height"])
        )
    def __init__(self,pos,health,speed,size,texture,border,title):
        self._pos = pos
        self._health = health
        self._speed = speed
        self._border = border
        self._size = size
        self._texture = texture
        self._title = title
        self.initVariables()
        self.initSprite()
    # Health System 
    def getTitle(self):
        return self._title
    def getHealth(self):
        return self._health
    def setHealth(self,value):
        self._health += value
    #Positions
    def move(self,move_pos):
        self._movePos = move_pos
    def getRect(self):
        return self._sprite.get_rect(topleft=(self._pos["x"],self._pos["y"]))
    def updatePositions(self,delta_time):
        self._pos["x"] += (self._movePos["x"] * self._speed * delta_time)
        self._pos["y"] += (self._movePos["y"] * self._speed * delta_time)

        if(self._pos["x"] >= self._border["width"] - self._size["width"]):
            self._pos["x"] = self._border["width"] - self._size["width"]
        
        elif(self._pos["x"] <= 0):
            self._pos["x"] = 0
        

        self._movePos["x"] = 0
    # Core
    def update(self,delta_time):
        self.updatePositions(delta_time)
    def render(self,window):
        window.blit(self._sprite, (self._pos["x"], self._pos["y"]))


    