import pygame
from src.gui.text import Text
from src.engine.scene import Scene


class MainScene(Scene):
    """Representing main screen"""
    def init_text(self):
        """Initialize variables of main screen"""
        x = self._size["width"] // 2
        y = self._size["height"] // 2

        self._text = Text(
            "Press Enter To Start",
            (255, 255, 255),
            32,
            "Courier New",
            {
                "x": x,
                "y": y,
            },
        )

    def __init__(
        self, background, window_width, window_height, set_scene
    ):
        self._size = {
            "width": window_width,
            "height": window_height,
        }
        self._set_scene = set_scene[0]
        self.init_text()
        super().__init__(background)

    def update(self, delta_time):
        """Update main screen"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._isRunning[0] = False
        self._keys = pygame.key.get_pressed()

        if self._keys[pygame.K_RETURN]:
            self._set_scene("GAME")

        super().update(delta_time)

    def render(self, window):
        """Render main screen"""
        window.fill(self._background)
        self._text.render(window)
