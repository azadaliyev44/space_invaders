import unittest
from src.engine.game_scene import GameScene
from src.entity.entity import Entity
from src.entity.enemy import Enemy
from src.entity.bullet import Bullet

class TestGameScene(unittest.TestCase):
    def test_entity_fields(self):
        entity = Entity({"x":300,"y":300}, 6, 100, {"width":300,"height":300}, "assets/images/enemy_boss.png", None, "nenon")
        entity.set_health(1)
        assert entity.get_health() == 7

    def test_update_enemies(self):
        with self.assertRaises(FileNotFoundError):
            enemy = Enemy((850, 300), 10, 5, (20, 20), "entity/enemy_boss.png", None, None)
            self.scene._enemies.append(enemy)
            self.scene.update_enemies(0.1)

    def test_bullet_update(self):
        bullet = Bullet({"x":5,"y":400})
        delta_time = 0.1
        bullet.update(delta_time)
        assert bullet.get_pos()["y"] == 350
        


if __name__ == '__main__':
    unittest.main()
