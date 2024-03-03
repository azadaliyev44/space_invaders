from src.entity.entity import Entity

class Player(Entity):
    def __init__(self, pos, health, speed, size, texture, border,title):
        super().__init__(pos, health, speed, size, texture, border,title)

    def update(self,delta_time):
        super().update(delta_time)