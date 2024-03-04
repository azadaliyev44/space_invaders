from src.entity.entity import Entity


class Enemy(Entity):
    """Representing enemies"""
    def __init__(self, pos, health, speed, size, texture, border, title):
        super().__init__(pos, health, speed, size, texture, border, title)

    def update(self, delta_time):
        """Update position of enemy"""
        super().move({"x": 0, "y": 1})
        super().update(delta_time)
