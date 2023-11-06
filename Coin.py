from pygame import *
import os

COIN_WIDTH = 20
COIN_HEIGHT = 20
ICON_DIR = os.path.dirname(__file__)
COIN_COLOR = "#DAA520"


class Coin(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((COIN_WIDTH, COIN_HEIGHT))
        self.image.fill(Color(COIN_COLOR))
        # self.image = image.load()
        # self.rect = Rect(x, y, COIN_WIDTH, COIN_HEIGHT)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
