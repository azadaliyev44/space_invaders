from src.entity.entity import Entity


class Player(Entity):
    """Representing player and its values"""
    def __init__(self, pos, health, speed, size, texture, border, title):
        super().__init__(pos, health, speed, size, texture, border, title)

    def update(self, delta_time):
        """Update player values"""
        super().update(delta_time)
