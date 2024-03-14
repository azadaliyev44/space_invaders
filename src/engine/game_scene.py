import random
import json

import pygame

from src.engine.scene import Scene
from src.entity.bullet import Bullet
from src.entity.enemy import Enemy
from src.entity.player import Player
from src.gui.healtbar import HealthBar
from src.gui.text import Text
from math import sqrt


class GameScene(Scene):
    """Representing game scene"""
    def __init__(self, background, win_width, win_height, pygame, is_running):
        super().__init__(background)
        self.win_width = win_width
        self.win_height = win_height
        self.pygame = pygame
        self._is_running = is_running
        self.init_variables()
        self.init_player()
        self.init_enemies()
        self.init_gui()
        self.init_audio()

    def init_audio(self):
        """Initialize audios"""
        self._audio["SHOOT"] = pygame.mixer.Sound(
            "./assets/sounds/shoot.wav")
        self._audio["ENEMY_DEATH"] = pygame.mixer.Sound(
            "./assets/sounds/enemy_dead.wav")
        self._audio["BOSS_DEATH"] = pygame.mixer.Sound(
            "./assets/sounds/boss_dead.wav")
        self._audio["BOSS_SPAWN"] = pygame.mixer.Sound(
            "./assets/sounds/boss_spawned.wav")
        self._audio["GAME_OVER"] = pygame.mixer.Sound(
            "./assets/sounds/game_over.wav")
        self._audio["HP_LOSS"] = pygame.mixer.Sound(
            "./assets/sounds/hp_loss.wav")

    def init_gui(self):
        """Initialize GUI"""
        self._ending_text = Text(
            "None", (255, 255, 255), 20, "Courier New",
            {"x": self.win_width // 2,
             "y": self.win_height // 2})
        self._gui["HEALTH_BAR"] = HealthBar(
            "./assets/images/hp.png",
            {"x": self.win_width, "y": self.win_height - 40},
            self._player.get_health())
        self._gui["LEVEL_TEXT"] = Text(
            "Level " + str(self._lvl), (255, 255, 255), 20, "Courier New",
            {"x": self.win_width - 50,
             "y": self.win_height - 20})
        self._gui["SCORE_TEXT"] = Text(
            "Score " + str(self._score), (255, 255, 255), 20, "Courier New",
            {"x": 50,
             "y": self.win_height - 20})

    def init_enemies(self):
        """Initialize enemies"""
        with open('./src/engine/entities.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
        self._enemies_types = data

    def init_player(self):
        """Initalize player"""
        self._player = Player(
            {"x": self.win_width // 2 - 40, "y": 620},
            3,
            300,
            {
                "width": 80,
                "height": 80,
            },
            "./assets/images/space_ship.png",
            {"width": self.win_width, "height": self.win_height},
            "Player",
        )

    def init_variables(self):
        """Initialize variables"""
        self._is_running = True
        self._keys = []
        # Bullets
        self._bullets = []
        self._shoot_timer = 0
        self._bullet_frequency = 0.22
        # Enemy
        self._enemies = []
        self._enemy_timer = 0
        self._enemy_freq = 1
        self._boss_spawn = False
        # Level,Score and Gui
        self._lvl = 1
        self._gui = {}
        self._score = 0
        self._audio = {}
        self._is_win = False
        self._is_lose = False

    def upgrade_enemies(self):
        """Update variables of enemies according to level"""
        for index in range(len(self._enemies_types)):
            init_health = self._enemies_types[index]["initial_health"]
            init_speed = self._enemies_types[index]["initial_speed"]
            new_health = init_health * 0.5 * self._lvl + 0.5
            new_speed = init_speed * sqrt(self._lvl)
            self._enemies_types[index]["health"] = new_health
            self._enemies_types[index]["speed"] = new_speed
            print(new_health)
            print(new_speed)

    # Update
    def update_boss(self):
        """Update boss variables"""
        if self._score == round(10 * 2.5**self._lvl) and not self._boss_spawn:
            self._audio["BOSS_SPAWN"].play(loops=0)
            self.set_backgorund((255, 0, 0))
            self._boss_spawn = True
            boss = self._enemies_types[3]
            self._enemies.append(self.enemy_template(boss))

    def update_enemies(self, delta_time):
        """Update enemy variables"""
        self.update_boss()
        self._enemy_timer += delta_time
        if self._enemy_timer > self._enemy_freq and not self._boss_spawn:
            self._enemy_timer = 0
            enemy_type = self._enemies_types[
                random.randrange(0, len(self._enemies_types) - 1)]
            self._enemies.append(self.enemy_template(enemy_type))
        for enemy in self._enemies:
            enemy.update(delta_time)
            enemy_rect = enemy.get_rect()
            player_rect = self._player.get_rect()
            self.check_enemy_colliderect(enemy, enemy_rect)
            if enemy.get_health() <= 0:
                self.enemy_remove(enemy)
            elif enemy_rect[1] >= self.win_height:
                self.enemy_pass(enemy)
            elif enemy_rect.colliderect(player_rect):
                self.game_over(enemy)

    def check_enemy_colliderect(self, enemy, enemy_rect):
        for bullet in self._bullets:
            bullet_rect = bullet.get_rect()
            if enemy_rect.colliderect(bullet_rect):
                self._score += 1
                self._bullets.remove(bullet)
                enemy.set_health(-1)
                self._gui["SCORE_TEXT"].set_text_content(
                    "Score " + str(self._score))

    def enemy_template(self, enemy_type):
        return Enemy({
            "x": random.randint(
                0,
                random.randint(
                    0, self.win_width - enemy_type["size"]["width"]
                ),
            ),
            "y": 0},
            enemy_type["health"],
            enemy_type["speed"],
            enemy_type["size"],
            enemy_type["texture"],
            {"width": self.win_width, "height": self.win_height},
            enemy_type["title"])

    def enemy_remove(self, enemy):
        self._enemies.remove(enemy)
        if enemy.get_title() == "BOSS":
            self._boss_spawn = False
            self._lvl += 1
            self._gui["LEVEL_TEXT"].set_text_content(
                "Level " + str(self._lvl)
            )
            self.set_backgorund((0, 0, 0))
            self._audio["BOSS_DEATH"].play(loops=0)
            self.upgrade_enemies()
        else:
            self._audio["ENEMY_DEATH"].play(loops=0)

    def enemy_pass(self, enemy):
        self._enemies.remove(enemy)
        self._player.set_health(-1)
        self._gui["HEALTH_BAR"].set_health(self._player.get_health())
        self._audio["HP_LOSS"].play(loops=0)

    def game_over(self, enemy):
        self._enemies.remove(enemy)
        self._player.set_health(-self._player.get_health())
        self._audio["GAME_OVER"].play(loops=0)

    def update_bullets(self, delta_time):
        """Update bullet variables"""
        self._shoot_timer += delta_time
        rect = self._player.get_rect()
        if self._shoot_timer >= self._bullet_frequency / sqrt(self._lvl):
            self._shoot_timer = 0
            self._bullets.append(
                Bullet({"x": rect[0] + rect[2] // 2, "y": rect[1]}))
            self._audio["SHOOT"].play(loops=0)

        for bullet in self._bullets:
            bullet.update(delta_time)
            if bullet.get_pos()["y"] <= 0:
                self._bullets.remove(bullet)

    def update_player(self, delta_time):
        """Update player varaibles"""
        self._player.update(delta_time)
        if self._player.get_health() <= 0:
            self._is_lose = True

    def update_events(self):
        """Handle running of game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._is_running[0] = False

        self._keys = pygame.key.get_pressed()

    def update_keys(self):
        """Controls"""
        if self._keys[pygame.K_a]:
            self._player.move({"x": -1, "y": 0})
        if self._keys[pygame.K_d]:
            self._player.move({"x": 1, "y": 0})
        if self._keys[pygame.K_ESCAPE]:
            self._is_running[0] = False

    def update(self, delta_time):
        """Update variables"""
        super().update()
        self.update_events()
        self.update_keys()
        self.update_player(delta_time)
        self.update_bullets(delta_time)
        self.update_enemies(delta_time)

        if self._lvl == 4:
            self._is_win = True

    def render(self, window):
        """Render game screen."""
        window.fill(self._background)
        self._player.render(window)
        for item in self._gui.values():
            item.render(window)
        for bullet in self._bullets:
            bullet.render(window)
        for enemy in self._enemies:
            enemy.render(window)
        if self._is_win or self._is_lose:
            if self._is_win:
                ending_message = "You Win, Your Score " + str(self._score)
            else:
                ending_message = "Game Over, Your Score " + str(self._score)
            self._ending_text.set_text_content(ending_message)
            window.fill(self._background)
            self._ending_text.render(window)
            pygame.display.update()
            pygame.time.delay(2000)
            self._is_running[0] = False
