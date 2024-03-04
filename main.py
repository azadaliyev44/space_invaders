import sys
import pygame
from src.game import Game

pygame.init()
pygame.display.set_caption("Space Invader (but fake)")

game = Game(500, 750, pygame)
game.run()

pygame.quit()
sys.exit()
