import pygame.sprite
from pygame import *
import os

COIN_WIDTH = 20
COIN_HEIGHT = 20
ICON_DIR = os.path.dirname(__file__)
COIN_COLOR = "#DAA520"


class Coin(sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((COIN_WIDTH, COIN_HEIGHT))
        self.image.fill(Color(COIN_COLOR))
        self.image = image.load('%s/sprites/coin/images.png' % ICON_DIR)
        # self.rect = Rect(x, y, COIN_WIDTH, COIN_HEIGHT)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(Color('#FFFFFF'))
        self.rect.x = x
        self.rect.y = y

    def update(self, Player):
        if pygame.sprite.collide_rect(self, Player):
            self.kill()
