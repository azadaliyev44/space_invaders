import pygame
class Bullet:
    # İnitialization
    def initVariables(self):
        self._speed = 500
    def initSprite(self):
        self._sprite = pygame.transform.scale(
            pygame.image.load("./assets/images/projectile.png"), (
                self._size["width"],
                self._size["height"],
            )
        )
    def __init__(self,pos):
        self._size = {
            "width" : 7,
            "height" : 15,
        }

        self._pos = {
            "x" : pos["x"] - self._size["width"] // 2,
            "y" : pos["y"]
        }
        self.initVariables()
        self.initSprite()
    # Accessors
    def getRect(self):
        return self._sprite.get_rect(topleft=(self._pos["x"],self._pos["y"]))
    def getPos(self):
        return self._pos
    # | CORE |   
    # Update
    def update(self,delta_time):
        self._pos["y"] -= delta_time * self._speed 
    # Render
    def render(self,window):
        window.blit(self._sprite,(
            self._pos["x"],
            self._pos["y"],
        ))    
