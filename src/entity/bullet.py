import pygame


class Bullet:
    """Representing Bullets"""

    def init_variables(self):
        """Initialize speed of bullets"""
        self._speed = 500

    def init_sprite(self):
        """Initialize texture of bullet"""
        self._sprite = pygame.transform.scale(
            pygame.image.load("./assets/images/projectile.png"),
            (
                self._size["width"],
                self._size["height"],
            ),
        )

    def __init__(self, pos):
        self._size = {
            "width": 7,
            "height": 15,
        }

        self._pos = {"x": pos["x"] - self._size["width"] // 2, "y": pos["y"]}
        self.init_variables()
        self.init_sprite()

    # Accessors
    def get_rect(self):
        """Get borders of bullets"""
        return self._sprite.get_rect(topleft=(self._pos["x"], self._pos["y"]))

    def get_pos(self):
        """Get position of bullets"""
        return self._pos

    # | CORE |
    # Update
    def update(self, delta_time):
        """Update position of bullet"""
        self._pos["y"] -= delta_time * self._speed

    # Render
    def render(self, window):
        """Render bullets"""
        window.blit(
            self._sprite,
            (
                self._pos["x"],
                self._pos["y"],
            ),
        )
