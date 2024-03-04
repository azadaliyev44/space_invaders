import pygame


class Scene:
    """Representing Screen"""
    def __init__(self, background):
        self._background = background

    # | Core |
    def update(self):
        """Update Screen"""
        pygame.display.update()

    def set_backgorund(self, color):
        """Set background color"""
        self._background = color

    def render(self, window):
        """Reset Screen"""
        window.fill(self._background)
