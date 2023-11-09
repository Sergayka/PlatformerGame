# import pygame.sprite
# from pygame import *
# import os
#
# COIN_WIDTH = 30
# COIN_HEIGHT = 30
# ICON_DIR = os.path.dirname(__file__)
# COIN_COLOR = "#DAA520"
# COLOR = "#FFFFFF"
#
#
# class Coin(sprite.Sprite):
#     def __init__(self, x, y):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = Surface((COIN_WIDTH, COIN_HEIGHT))
#         self.image.fill(Color(COIN_COLOR))
#         self.image = image.load("%s/sprites/coin/coin.png" % ICON_DIR)
#         self.image.set_colorkey(Color(COLOR))
#         self.rect = Rect(x, y, COIN_WIDTH, COIN_HEIGHT)
#
#     def update(self, Player):
#         if pygame.sprite.collide_rect(self, Player):
#             self.kill()