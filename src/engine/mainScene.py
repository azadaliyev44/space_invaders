import pygame
from src.gui.text import Text
from src.engine.scene import Scene
class MainScene(Scene):
    def initText(self):
        x = self._size["width"] // 2
        y = self._size["height"] // 2

        self._text = Text(
            "Press Enter To Start",
            (255,255,255),
            32,
            "Courier New",
            {
                "x" : x,
                "y" : y,
            }
        )
    def __init__(self,background,window_width, window_height,pygame,isRunning,setScene):
        self._size = {
            "width": window_width,
            "height": window_height,
        }
        self._setScene = setScene[0]
        self.initText()
        super().__init__(background)
    def update(self,delta_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._isRunning[0] = False
        self._keys = pygame.key.get_pressed() 

        if self._keys[pygame.K_RETURN]:
            self._setScene("GAME")
            
        super().update(delta_time)
    def render(self,window):
        window.fill(self._background)
        self._text.render(window)