# import pygame.sprite
# from pygame import *
# import os
#
# ICON_DIR = os.path.dirname(__file__)
#
# FIRESHOOT_WIDTH = 16
# FIRESHOOT_HEIGHT = 16
#
# FIRESHOOT_COLOR = "#DAA520"
#
#
# class FireProjectile(sprite.Sprite):
#     def __init__(self, x, y):
#         sprite.Sprite.__init__(self)
#         self.image = Surface((FIRESHOOT_WIDTH, FIRESHOOT_COLOR))
#         self.image.fill(Color(FIRESHOOT_COLOR))
#         # self.image = image.load("%s/sprites/fireblock/fireshoot.png" % ICON_DIR)
#         self.rect = Rect(x, y, FIRESHOOT_WIDTH, FIRESHOOT_HEIGHT)
#         self.speed = 6
#
#     def update(self):
#         self.rect.x += self.speed
