#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame.sprite
from pygame import *
import os

"""
Можно, но не рекомендуется поиграться с размерами платформ (13-14 строки), однако может привезти к небольшому полому границ,
Мы можем изменить / убрать изображение платфомы(строка 24), если убираем, то играться с ее цветом (разкомент 23 и играем в 15 строке) 
"""

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
# PLATFORM_COLOR = "#FFFFFF"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        # self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/sprites/blocks/stone_bricks.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


COIN_WIDTH = 30
COIN_HEIGHT = 30
COIN_COLOR = "#DAA520"
COLOR = "#FFFFFF"


class Coin(sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((COIN_WIDTH, COIN_HEIGHT))
        self.image.fill(Color(COIN_COLOR))
        self.image = image.load("%s/sprites/coin/golden_ingot.png" % ICON_DIR)
        self.image.set_colorkey(Color(COLOR))
        self.rect = Rect(x, y, COIN_WIDTH, COIN_HEIGHT)

    def update(self, Player):
        if pygame.sprite.collide_rect(self, Player):
            self.kill()


FIREBLOCK_WIDTH = 32
FIREBLOCK_HEIGHT = 32

FIREBLOCK_COLOR = "#DAA520"


class FireBlock(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((FIREBLOCK_WIDTH, FIREBLOCK_HEIGHT))
        self.image = image.load("%s/sprites/blocks/dispencer.png" % ICON_DIR)
        # self.image.fill(Color(FIREBLOCK_COLOR))
        self.rect = Rect(x, y, FIREBLOCK_WIDTH, FIREBLOCK_HEIGHT)

        # self.projectile = FireProjectile(x, y)
        # self.projectile.rect.x = self.rect.x
        # self.projectile.rect.y = self.rect.y
        self.fire_projectiles = pygame.sprite.Group()
        self.create_fire_projectiles(x, y)

        self.fire_timer = 0
        self.fire_interval = 2000

    def create_fire_projectiles(self, x, y):
        # fire_projectile = FireProjectile(x, y)
        fire_projectile_right = FireProjectile(self.rect.x, self.rect.y, speed=0.5)
        fire_projectile_left = FireProjectile(self.rect.x, self.rect.y, speed=-0.8)

        # fire_projectile_right.rect.move_ip(self.rect.x, self.rect.y)
        # fire_projectile_left.rect.move_ip(self.rect.x, self.rect.y)
        self.fire_projectiles.add(fire_projectile_right, fire_projectile_left)

    def update(self, Player):
        current_time = pygame.time.get_ticks()
        if current_time - self.fire_timer > self.fire_interval:
            self.fire_timer = current_time
            self.create_fire_projectiles(self.rect.x, self.rect.y)
        # self.projectile.update()
        # if pygame.sprite.collide_rect(self.projectile, Player):
        #     raise SystemExit('gg')
        for fire_projectile in self.fire_projectiles:
            fire_projectile.update()
            if pygame.sprite.collide_rect(fire_projectile, Player):
                raise SystemExit('gg')


FIREPROJECTILE_WIDTH = 10
FIREPROJECTILE_HEIGHT = 10
FIREPROJECTILE_COLOR = "#0FFFA7"


class FireProjectile(sprite.Sprite):
    def __init__(self, x, y, speed):
        sprite.Sprite.__init__(self)
        self.image = Surface((FIREPROJECTILE_WIDTH, FIREPROJECTILE_HEIGHT))
        self.image = image.load("%s/sprites/blocks/fireball.png" % ICON_DIR)
        # self.image.fill(Color(FIREPROJECTILE_COLOR))
        self.rect = Rect(x, y, FIREPROJECTILE_WIDTH, FIREPROJECTILE_HEIGHT)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed


class Thorn(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        # self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/sprites/blocks/lava.png" % ICON_DIR)
        # self.image.set_colorkey(Color('#FFFFFF'))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def update(self, Player):
        if pygame.sprite.collide_rect(self, Player):
            raise SystemExit('End')
