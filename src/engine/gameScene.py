import random
import math
from src.engine.scene import Scene
from src.entity.player import Player
from src.entity.bullet import Bullet
from src.entity.enemy import Enemy
from src.gui.text import Text
from src.gui.healtbar import HealthBar

class GameScene(Scene):
    def initAudio(self):
        self._audio["SHOOT"] = self.pygame.mixer.Sound("./assets/sounds/shoot.wav")
        self._audio["ENEMY_DEATH"] = self.pygame.mixer.Sound("./assets/sounds/enemy_dead.wav")
        self._audio["BOSS_DEATH"] = self.pygame.mixer.Sound("./assets/sounds/boss_dead.wav")
        self._audio["BOSS_SPAWN"] = self.pygame.mixer.Sound("./assets/sounds/boss_spawned.wav")
        self._audio["GAME_OVER"] = self.pygame.mixer.Sound("./assets/sounds/game_over.wav")
        self._audio["HP_LOSS"] = self.pygame.mixer.Sound("./assets/sounds/hp_loss.wav")
    def initGui(self):
        self._endingText = Text(
            "None",
            (255,255,255),
            20,
            "Courier New",
            {
                "x":self.window_width//2,
                "y":self.window_height//2,
            }
        )  
        self._gui["HEALTH_BAR"] = HealthBar(
            "./assets/images/hp.png",
            {
                "x" : self.window_width,
                "y" : self.window_height - 40
            },
            self._player.getHealth()
        )
        self._gui["LEVEL_TEXT"] = Text(
            "Level " + str(self._level),
            (255,255,255),
            20,
            "Courier New",
            {
                "x":self.window_width - 50,
                "y":self.window_height - 20,
            }
        )  
        self._gui["SCORE_TEXT"] = Text(
            "Score " + str(self._score),
            (255,255,255),
            20,
            "Courier New",
            {
                "x":50,
                "y":self.window_height - 20,
            }
        )  
    def initEnemies(self):
        self._enemiesTypes = [
            {
                "title" : "DRONE",
                "texture" : "./assets/images/enemy_drone.png",
                "size" : {"width":80,"height":40},
                "health" : 2,
                "speed": 200,
            },
            {
                "title" : "SPACE_SHIP",
                "texture" : "./assets/images/enemy_space_ship.png",
                "size" : {"width":80,"height":80},
                "health" : 6,
                "speed": 50,
            },
            {
                "title" : "UFO",
                "texture" : "./assets/images/enemy_ufo.png",
                "size" : {"width":80,"height":60},
                "health" : 4,
                "speed": 100,
            },
            {
                "title" : "BOSS",
                "texture" : "./assets/images/enemy_boss.png",
                "size" : {"width":160,"height":160},
                "health" : 15,
                "speed": 50,
            },
        ]
    def initPlayer(self):
        self._player = Player(
            {
                "x":self.window_width // 2 - 40,
                "y":620
            },
            3,
            300,
            {
                "width":80,
                "height":80,
            },
            "./assets/images/space_ship.png",
            {
                "width":self.window_width,
                "height":self.window_height
            },
            "Player"
    )
    def initVariables(self):
        self._isRunning = True
        self._keys = []

        # Bullets
        self._bullets = []
        self._shootTimer = 0
        self._bulletFrequency = 0.3
        #Enemy
        self._enemies = []
        self._enemySpawnTimer = 0
        self._enemyFrequency = 1
        self._bossSpawned = False
        # Level,Score and Gui 
        self._level = 1
        self._gui = {}
        self._score = 0
        self._audio = {}
        self._isWin = False
        self._isLose = False
    def __init__(self,background,window_width, window_height,pygame,isRunning,setScene):
        super().__init__(background)
        self.window_width = window_width
        self.window_height = window_height
        self.pygame = pygame
        self._isRunning = isRunning
        self.initVariables()
        self.initPlayer()
        self.initEnemies()
        self.initGui()
        self.initAudio()
    def upgradeEnemies(self):
            self._enemiesTypes = [
            {
                "title" : "DRONE",
                "texture" : "./assets/images/enemy_drone.png",
                "size" : {"width":80,"height":40},
                "health" : 2 * 0.5 * self._level + 0.5 ,
                "speed": 200 * math.sqrt(self._level),
            },
            {
                "title" : "SPACE_SHIP",
                "texture" : "./assets/images/enemy_space_ship.png",
                "size" : {"width":80,"height":80},
                "health" : 6 * 0.5 * self._level + 0.5 ,
                "speed": 50 * math.sqrt(self._level),
            },
            {
                "title" : "UFO",
                "texture" : "./assets/images/enemy_ufo.png",
                "size" : {"width":80,"height":60},
                "health" : 4 * 0.5 * self._level + 0.5 ,
                "speed": 100 * math.sqrt(self._level),
            },
            {
                "title" : "BOSS",
                "texture" : "./assets/images/enemy_boss.png",
                "size" : {"width":160,"height":160},
                "health" : 15 * 0.5 * self._level + 0.5 ,
                "speed": 50 * math.sqrt(self._level),
            },
        ]
    # Update
    def updateBoss(self):
        if self._score == round(10 * 2.5 ** self._level) and not self._bossSpawned:
            self._audio["BOSS_SPAWN"].play(loops=0)
            self.setBackgorund((255,0,0))
            self._bossSpawned = True
            boss = self._enemiesTypes[3]
            self._enemies.append(Enemy(
                    {
                        # Bura Bax
                        "x" : random.randint(0,random.randint(0,self.window_width - boss["size"]["width"])),
                        "y":0,
                    },
                    boss["health"],
                    boss["speed"],
                    boss["size"],
                    boss["texture"],
                    {
                        "width":self.window_width,
                        "height":self.window_height
                    },
                    boss["title"]
                ))
    def updateEnemies(self,delta_time):
        self.updateBoss()
        self._enemySpawnTimer += delta_time
        if(self._enemySpawnTimer > self._enemyFrequency and not self._bossSpawned):
            self._enemySpawnTimer = 0
            enemyType = self._enemiesTypes[random.randrange(0,len(self._enemiesTypes) - 1)]
            self._enemies.append(Enemy(
                {
                    "x" : random.randint(0,random.randint(0,self.window_width - enemyType["size"]["width"])),
                    "y":0,
                },
                enemyType["health"],
                enemyType["speed"],
                enemyType["size"],
                enemyType["texture"],
                {
                    "width":self.window_width,
                    "height":self.window_height
                },
                enemyType["title"]
            ))
        for enemy in self._enemies:
            enemyRect = enemy.getRect()
            playerRect = self._player.getRect()
            enemy.update(delta_time) 
            for bullet in self._bullets:
                bulletRect = bullet.getRect()
                # Update Et bunu
                if enemyRect.colliderect(bulletRect):
                    self._score += 1
                    self._bullets.remove(bullet)
                    enemy.setHealth(-1)
                    self._gui["SCORE_TEXT"].setTextContent("Score " + str(self._score))
            if enemy.getHealth() <= 0:
                self._enemies.remove(enemy)
                if enemy.getTitle() == "BOSS":
                    self._bossSpawned = False
                    self._level += 1
                    self._gui["LEVEL_TEXT"].setTextContent("Level " + str(self._level))
                    self.setBackgorund((0,0,0))
                    self._audio["BOSS_DEATH"].play(loops=0)
                    self.upgradeEnemies()
                else:
                    self._audio["ENEMY_DEATH"].play(loops=0)
                    
            elif enemyRect[1] >= self.window_height:
                self._enemies.remove(enemy)
                self._player.setHealth(-1)
                self._gui["HEALTH_BAR"].setHealth(self._player.getHealth())
                self._audio["HP_LOSS"].play(loops=0)
            elif enemyRect.colliderect(playerRect):
                self._enemies.remove(enemy)
                self._player.setHealth(-self._player.getHealth())
                self._audio["GAME_OVER"].play(loops=0)
    def updateBullets(self,delta_time):
        self._shootTimer += delta_time
        rect = self._player.getRect()
        if self._shootTimer >= self._bulletFrequency / math.sqrt(self._level):
                self._shootTimer = 0
                self._bullets.append(Bullet(
                    {
                        "x": rect[0] + rect[2] // 2,
                        "y": rect[1]
                    }))
                self._audio["SHOOT"].play(loops=0)
                
        for bullet in self._bullets:
            bullet.update(delta_time)
            if bullet.getPos()["y"] <= 0:
                self._bullets.remove(bullet)  
    def updatePlayer(self,delta_time):
        self._player.update(delta_time)
        if self._player.getHealth() <= 0:
            self._isLose = True
    def updateEvents(self):
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self._isRunning[0] = False
        
        self._keys = self.pygame.key.get_pressed() 
    def updateKeys(self):
        if self._keys[self.pygame.K_a]:
            self._player.move({"x":-1,"y":0})
        if self._keys[self.pygame.K_d]:
            self._player.move({"x":1,"y":0})   
        if self._keys[self.pygame.K_ESCAPE]:
            self._isRunning[0] = False
    def update(self,delta_time):
        super().update(delta_time)
        self.updateEvents()
        self.updateKeys()
        self.updatePlayer(delta_time)
        self.updateBullets(delta_time)
        self.updateEnemies(delta_time)

        if(self._level == 4):
            self._isWin = True
    def render(self,window):
        window.fill(self._background)
        self._player.render(window)
        # Render Bullets
        for item in self._gui:
            self._gui[item].render(window)
        for bullet in self._bullets:
            bullet.render(window)
        for enemy in self._enemies:
            enemy.render(window)

        if(self._isWin or self._isLose):
            if(self._isWin):
                self._endingText.setTextContent("You Win, Your Score " + str(self._score))
            elif(self._isLose):  
                self._endingText.setTextContent("Game Over, Your Score " + str(self._score))
            window.fill(self._background)
            self._endingText.render(window)
            self.pygame.display.update()
            self.pygame.time.delay(2000)
            self._isRunning[0] = False
