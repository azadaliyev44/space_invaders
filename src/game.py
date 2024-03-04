from src.engine.game_scene import GameScene
from src.engine.main_scene import MainScene


class Game:
    def init_window(self):
        """Initialize the game window"""
        self._window = self._pygame.display.set_mode(
            (self._size["width"], self._size["height"])
        )

    def __init__(self, width, height, pygame):
        self._pygame = pygame
        self._size = {"width": width, "height": height}
        # Delta Time
        self.init_window()
        self._clock = pygame.time.Clock()
        self._FPS = 60
        self._running = [True]
        self._current_scene = MainScene(
            (0, 0, 0), width, height, pygame, self._running, [self.set_scene]
        )

    def set_scene(self, name):
        """Set the scene"""
        if name == "MAIN":
            self._current_scene = MainScene(
                "black",
                self._size["width"],
                self._size["height"],
                self._pygame,
                self._running,
                [self.set_scene],
            )
        elif name == "GAME":
            self._current_scene = GameScene(
                "black",
                self._size["width"],
                self._size["height"],
                self._pygame,
                self._running,
                [self.set_scene],
            )

    # Core
    def run(self):
        """Run the game process"""
        self._clock.tick(self._FPS)
        while self._running:
            delta_time = self._clock.tick(self._FPS) / 1000.0
            self._current_scene.update(delta_time)
            self._current_scene.render(self._window)
