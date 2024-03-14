import pygame


class HealthBar:
    """Representing healthbar"""

    def init_sprite(self):
        """Initialize Sprite of healthbar"""
        self._sprite = pygame.transform.scale(
            pygame.image.load(self._texture),
            (self._size["width"], self._size["height"]),
        )

    def __init__(self, texture, pos, health):
        self._texture = texture
        self._pos = pos
        self._size = {"width": 30, "height": 30}
        self._health = health
        self.init_sprite()

    def set_health(self, health):
        """Set new value for player health"""
        self._health = health

    def update_pos(self, pos):
        """Update position of healthbar"""
        self._pos = pos

    def render(self, window):
        """Render healthbar on the screen"""
        offset_x = 5
        pos_x = (self._pos["x"] - self._health *
                 (self._size["width"] + offset_x)) // 2
        pos_y = self._pos["y"]
        for i in range(self._health):
            window.blit(
                self._sprite, (pos_x + i *
                               self._size["width"] + offset_x, pos_y)
            )
