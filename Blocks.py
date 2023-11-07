#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import pygame.sprite
from pygame import *
import os

"""
Можно, но не рекомендуется поиграться с размерами платформ (13-14 строки), однако может привезти к небольшому полому границ,
Мы можем изменить / убрать изображение платфомы(строка 24), если убираем, то играться с ее цветом (разкомент 23 и играем в 15 строке) 
"""


PLATFORM_WIDTH = 33
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FFFFFF"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        # self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/sprites/blocks/platform2.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Cloud(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        # self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/sprites/blocks/platform.png" % ICON_DIR)
        self.image.set_colorkey(Color('#FFFFFF'))

        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Thorn(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        # self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/sprites/blocks/36086.png" % ICON_DIR)
        self.image.set_colorkey(Color('#FFFFFF'))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def update(self, Player):
        if pygame.sprite.collide_rect(self, Player):
            sys.exit()
