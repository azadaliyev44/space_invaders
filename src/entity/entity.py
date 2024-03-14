import pygame


class Entity:
    """Representing entities"""

    def init_variables(self):
        """Initialize position of entities"""
        self._move_pos = {"x": 0, "y": 0}

    def init_sprite(self):
        """Initialize texture of entities"""
        self._sprite = pygame.transform.scale(
            pygame.image.load(self._texture),
            (self._size["width"], self._size["height"]),
        )

    def __init__(self, pos, health, speed, size, texture, border, title):
        self._pos = pos
        self._health = health
        self._speed = speed
        self._border = border
        self._size = size
        self._texture = texture
        self._title = title
        self.init_variables()
        self.init_sprite()

    # Health System
    def get_title(self):
        return self._title

    def get_health(self):
        """Get health of entities"""
        return self._health

    def set_health(self, value):
        """Set health for entities"""
        self._health += value

    # Positions
    def move(self, move_pos):
        """Move entities"""
        self._move_pos = move_pos

    def get_rect(self):
        """Get borders of entities"""
        return self._sprite.get_rect(topleft=(self._pos["x"], self._pos["y"]))

    def update_positions(self, delta_time):
        """Update positions of entities"""
        self._pos["x"] += self._move_pos["x"] * self._speed * delta_time
        self._pos["y"] += self._move_pos["y"] * self._speed * delta_time

        if self._pos["x"] >= self._border["width"] - self._size["width"]:
            self._pos["x"] = self._border["width"] - self._size["width"]

        elif self._pos["x"] <= 0:
            self._pos["x"] = 0

        self._move_pos["x"] = 0

    # Core
    def update(self, delta_time):
        """Update entities"""
        self.update_positions(delta_time)

    def render(self, window):
        """Render enetities on the screen"""
        window.blit(self._sprite, (self._pos["x"], self._pos["y"]))
