import pygame

class Scene:
    def __init__(self,background):
        self._background = background
    # | Core | 
    def update(self,delta_time):
        pygame.display.update()
        pass
    def setBackgorund(self,color):
        self._background = color
    def render(self,window):
        # Reset window
        window.fill(self._background)