import pygame
class HealthBar:
    def initSprite(self):
        self._sprite = pygame.transform.scale(
            pygame.image.load(self._texture), 
            (self._size["width"], self._size["height"])
        )
    def __init__(self,texture,pos,health):
        self._texture = texture
        self._pos = pos
        self._size = {
            "width" : 30,
            "height" : 30
        }
        self._health = health
        self.initSprite()
    def setHealth(self,health):
        self._health = health
    def updatePos(self,pos):
        self._pos = pos
    def render(self,window):
        offsetX = 5
        posX = (self._pos["x"] - self._health * (self._size["width"] + offsetX)) // 2
        posY = self._pos["y"]
        for i in range(self._health):
            window.blit(self._sprite,(posX + i * self._size["width"] + offsetX,posY))