import pygame


class Text:
    """Representing texts on screen"""

    def init_text(self):
        """Initialize text on the screen"""
        font = pygame.font.SysFont(self._font_family, self._font_size)
        self._text = font.render(self._content, True, self._color)

    def __init__(self, content, color, font_size, font_family, pos):
        self._content = content
        self._color = color
        self._font_size = font_size
        self._font_family = font_family
        self._pos = pos
        self.init_text()

        self.set_position()

    def set_position(self):
        """Set position of Text"""
        self._rect = self._text.get_rect()
        self._rect.center = (self._pos["x"], self._pos["y"])

    def set_text_content(self, value):
        """Set content for Texts"""
        self._content = value
        self.init_text()
        self.set_position()

    def render(self, window):
        """Render the Window"""
        window.blit(self._text, self._rect)
