import random
import math
from src.engine.scene import Scene
from src.entity.player import Player
from src.entity.bullet import Bullet
from src.entity.enemy import Enemy
from src.gui.text import Text
from src.gui.healtbar import HealthBar


class GameScene(Scene):
    """Representing game scene"""
    def init_audio(self):
        """Initialize audios"""
        self._audio["SHOOT"] = self.pygame.mixer.Sound("./assets/sounds/shoot.wav")
        self._audio["ENEMY_DEATH"] = self.pygame.mixer.Sound(
            "./assets/sounds/enemy_dead.wav"
        )
        self._audio["BOSS_DEATH"] = self.pygame.mixer.Sound(
            "./assets/sounds/boss_dead.wav"
        )
        self._audio["BOSS_SPAWN"] = self.pygame.mixer.Sound(
            "./assets/sounds/boss_spawned.wav"
        )
        self._audio["GAME_OVER"] = self.pygame.mixer.Sound(
            "./assets/sounds/game_over.wav"
        )
        self._audio["HP_LOSS"] = self.pygame.mixer.Sound("./assets/sounds/hp_loss.wav")

    def init_gui(self):
        """Initialize GUI"""
        self._ending_text = Text(
            "None",
            (255, 255, 255),
            20,
            "Courier New",
            {
                "x": self.window_width // 2,
                "y": self.window_height // 2,
            },
        )
        self._gui["HEALTH_BAR"] = HealthBar(
            "./assets/images/hp.png",
            {"x": self.window_width, "y": self.window_height - 40},
            self._player.getHealth(),
        )
        self._gui["LEVEL_TEXT"] = Text(
            "Level " + str(self._level),
            (255, 255, 255),
            20,
            "Courier New",
            {
                "x": self.window_width - 50,
                "y": self.window_height - 20,
            },
        )
        self._gui["SCORE_TEXT"] = Text(
            "Score " + str(self._score),
            (255, 255, 255),
            20,
            "Courier New",
            {
                "x": 50,
                "y": self.window_height - 20,
            },
        )

    def init_enemies(self):
        """Initialize enemies"""
        self._enemies_types = [
            {
                "title": "DRONE",
                "texture": "./assets/images/enemy_drone.png",
                "size": {"width": 80, "height": 40},
                "health": 2,
                "speed": 200,
            },
            {
                "title": "SPACE_SHIP",
                "texture": "./assets/images/enemy_space_ship.png",
                "size": {"width": 80, "height": 80},
                "health": 6,
                "speed": 50,
            },
            {
                "title": "UFO",
                "texture": "./assets/images/enemy_ufo.png",
                "size": {"width": 80, "height": 60},
                "health": 4,
                "speed": 100,
            },
            {
                "title": "BOSS",
                "texture": "./assets/images/enemy_boss.png",
                "size": {"width": 160, "height": 160},
                "health": 15,
                "speed": 50,
            },
        ]

    def init_player(self):
        """Initalize player"""
        self._player = Player(
            {"x": self.window_width // 2 - 40, "y": 620},
            3,
            300,
            {
                "width": 80,
                "height": 80,
            },
            "./assets/images/space_ship.png",
            {"width": self.window_width, "height": self.window_height},
            "Player",
        )

    def init_variables(self):
        """Initialize variables"""
        self._is_running = True
        self._keys = []

        # Bullets
        self._bullets = []
        self._shoot_timer = 0
        self._bullet_frequency = 0.3
        # Enemy
        self._enemies = []
        self._enemy_spawn_timer = 0
        self._enemy_frequency = 1
        self._boss_spawned = False
        # Level,Score and Gui
        self._level = 1
        self._gui = {}
        self._score = 0
        self._audio = {}
        self._is_win = False
        self._is_lose = False

    def __init__(
        self, background, window_width, window_height, pygame, is_running
    ):
        super().__init__(background)
        self.window_width = window_width
        self.window_height = window_height
        self.pygame = pygame
        self._is_running = is_running
        self.init_variables()
        self.init_player()
        self.init_enemies()
        self.init_gui()
        self.init_audio()

    def upgrade_enemies(self):
        """Update variables of enemies according to level"""
        self._enemies_types = [
            {
                "title": "DRONE",
                "texture": "./assets/images/enemy_drone.png",
                "size": {"width": 80, "height": 40},
                "health": 2 * 0.5 * self._level + 0.5,
                "speed": 200 * math.sqrt(self._level),
            },
            {
                "title": "SPACE_SHIP",
                "texture": "./assets/images/enemy_space_ship.png",
                "size": {"width": 80, "height": 80},
                "health": 6 * 0.5 * self._level + 0.5,
                "speed": 50 * math.sqrt(self._level),
            },
            {
                "title": "UFO",
                "texture": "./assets/images/enemy_ufo.png",
                "size": {"width": 80, "height": 60},
                "health": 4 * 0.5 * self._level + 0.5,
                "speed": 100 * math.sqrt(self._level),
            },
            {
                "title": "BOSS",
                "texture": "./assets/images/enemy_boss.png",
                "size": {"width": 160, "height": 160},
                "health": 15 * 0.5 * self._level + 0.5,
                "speed": 50 * math.sqrt(self._level),
            },
        ]

    # Update
    def update_boss(self):
        """Update boss variables"""
        if self._score == round(10 * 2.5**self._level) and not self._boss_spawned:
            self._audio["BOSS_SPAWN"].play(loops=0)
            self.setBackgorund((255, 0, 0))
            self._boss_spawned = True
            boss = self._enemies_types[3]
            self._enemies.append(
                Enemy(
                    {
                        "x": random.randint(
                            0,
                            random.randint(
                                0, self.window_width - boss["size"]["width"]
                            ),
                        ),
                        "y": 0,
                    },
                    boss["health"],
                    boss["speed"],
                    boss["size"],
                    boss["texture"],
                    {"width": self.window_width, "height": self.window_height},
                    boss["title"],
                )
            )

    def update_enemies(self, delta_time):
        """Update enemy variables"""
        self.update_boss()
        self._enemy_spawn_timer += delta_time
        if self._enemy_spawn_timer > self._enemy_frequency and not self._boss_spawned:
            self._enemy_spawn_timer = 0
            enemy_type = self._enemies_types[
                random.randrange(0, len(self._enemies_types) - 1)
            ]
            self._enemies.append(
                Enemy(
                    {
                        "x": random.randint(
                            0,
                            random.randint(
                                0, self.window_width - enemy_type["size"]["width"]
                            ),
                        ),
                        "y": 0,
                    },
                    enemy_type["health"],
                    enemy_type["speed"],
                    enemy_type["size"],
                    enemy_type["texture"],
                    {"width": self.window_width, "height": self.window_height},
                    enemy_type["title"],
                )
            )
        for enemy in self._enemies:
            enemy_rect = enemy.get_rect()
            player_rect = self._player.get_rect()
            enemy.update(delta_time)
            for bullet in self._bullets:
                bullet_rect = bullet.get_rect()
                # Update Et bunu
                if enemy_rect.colliderect(bullet_rect):
                    self._score += 1
                    self._bullets.remove(bullet)
                    enemy.setHealth(-1)
                    self._gui["SCORE_TEXT"].setTextContent("Score " + str(self._score))
            if enemy.getHealth() <= 0:
                self._enemies.remove(enemy)
                if enemy.getTitle() == "BOSS":
                    self._boss_spawned = False
                    self._level += 1
                    self._gui["LEVEL_TEXT"].setTextContent("Level " + str(self._level))
                    self.setBackgorund((0, 0, 0))
                    self._audio["BOSS_DEATH"].play(loops=0)
                    self.upgrade_enemies()
                else:
                    self._audio["ENEMY_DEATH"].play(loops=0)

            elif enemy_rect[1] >= self.window_height:
                self._enemies.remove(enemy)
                self._player.setHealth(-1)
                self._gui["HEALTH_BAR"].setHealth(self._player.getHealth())
                self._audio["HP_LOSS"].play(loops=0)
            elif enemy_rect.colliderect(player_rect):
                self._enemies.remove(enemy)
                self._player.setHealth(-self._player.getHealth())
                self._audio["GAME_OVER"].play(loops=0)

    def update_bullets(self, delta_time):
        """Update bullet variables"""
        self._shoot_timer += delta_time
        rect = self._player.get_rect()
        if self._shoot_timer >= self._bullet_frequency / math.sqrt(self._level):
            self._shoot_timer = 0
            self._bullets.append(Bullet({"x": rect[0] + rect[2] // 2, "y": rect[1]}))
            self._audio["SHOOT"].play(loops=0)

        for bullet in self._bullets:
            bullet.update(delta_time)
            if bullet.getPos()["y"] <= 0:
                self._bullets.remove(bullet)

    def update_player(self, delta_time):
        """Update player varaibles"""
        self._player.update(delta_time)
        if self._player.getHealth() <= 0:
            self._is_lose = True

    def update_events(self):
        """Handle running of game"""
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self._is_running[0] = False

        self._keys = self.pygame.key.get_pressed()

    def update_keys(self):
        """Controls"""
        if self._keys[self.pygame.K_a]:
            self._player.move({"x": -1, "y": 0})
        if self._keys[self.pygame.K_d]:
            self._player.move({"x": 1, "y": 0})
        if self._keys[self.pygame.K_ESCAPE]:
            self._is_running[0] = False

    def update(self, delta_time):
        """Update variables"""
        super().update(delta_time)
        self.update_events()
        self.update_keys()
        self.update_player(delta_time)
        self.update_bullets(delta_time)
        self.update_enemies(delta_time)

        if self._level == 4:
            self._is_win = True

    def render(self, window):
        """Render game screen"""
        window.fill(self._background)
        self._player.render(window)
        # Render Bullets
        for item in self._gui:
            self._gui[item].render(window)
        for bullet in self._bullets:
            bullet.render(window)
        for enemy in self._enemies:
            enemy.render(window)

        if self._is_win or self._is_lose:
            if self._is_win:
                self._ending_text.setTextContent(
                    "You Win, Your Score " + str(self._score)
                )
            elif self._is_lose:
                self._ending_text.setTextContent(
                    "Game Over, Your Score " + str(self._score)
                )
            window.fill(self._background)
            self._ending_text.render(window)
            self.pygame.display.update()
            self.pygame.time.delay(2000)
            self._is_running[0] = False
