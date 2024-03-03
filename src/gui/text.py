import pygame
class Text:
    def initText(self):
        font = pygame.font.SysFont(self._fontFamily, self._fontSize)
        self._text = font.render(self._content,True,self._color)
    def __init__(self,content,color,font_size,font_family,pos):
        self._content = content
        self._color = color
        self._fontSize = font_size
        self._fontFamily = font_family
        self._pos = pos
        self.initText()
        
        self.setPosition()
    def setPosition(self):
        self._rect = self._text.get_rect()
        self._rect.center = (self._pos["x"],self._pos["y"])

    def setTextContent(self,value):
        self._content = value
        self.initText()
        self.setPosition()
    def update(self,window):
        pass
    def render(self,window):
        window.blit(self._text,self._rect)