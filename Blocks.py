#!/usr/bin/env python
# -*- coding: utf-8 -*-

from platformer import *
import pygame.sprite
from pygame import *
import os


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

        self.image = image.load("%s/sprites/coin/coin.png" % ICON_DIR)

        self.image.set_colorkey(Color(COLOR))
        self.rect = Rect(x, y, COIN_WIDTH, COIN_HEIGHT)

    def update(self, player):
        if pygame.sprite.collide_rect(self, player):
            self.kill()


FIREBLOCK_WIDTH = 32
FIREBLOCK_HEIGHT = 32

FIREBLOCK_COLOR = "#DAA520"


class ShootingBlock(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((FIREBLOCK_WIDTH, FIREBLOCK_HEIGHT))
        self.image = image.load("%s/sprites/blocks/dispencer.png" % ICON_DIR)
        # self.image.fill(Color(FIREBLOCK_COLOR))
        self.rect = Rect(x, y, FIREBLOCK_WIDTH, FIREBLOCK_HEIGHT)

        self.fire_projectiles = pygame.sprite.Group()
        self.create_projectiles(x, y)

        self.fire_timer = 0
        self.fire_interval = 2000

    def create_projectiles(self, x, y):
        projectile_right = Projectiles(self.rect.x + 34, self.rect.y + 9, speed=1)
        projectile_left = Projectiles(self.rect.x - 19, self.rect.y + 9, speed=-1)

        self.fire_projectiles.add(projectile_right, projectile_left)

    def update(self, player, platforms, thorns, fire_blocks):
        current_time = pygame.time.get_ticks()
        if current_time - self.fire_timer > self.fire_interval:
            self.fire_timer = current_time
            self.create_projectiles(self.rect.x, self.rect.y)

        for fire_projectile in self.fire_projectiles:
            fire_projectile.update()
            if pygame.sprite.collide_rect(fire_projectile, player):
                return True

            if pygame.sprite.spritecollide(fire_projectile, platforms, False) or \
                    pygame.sprite.spritecollide(fire_projectile, thorns, False) or \
                    pygame.sprite.spritecollide(fire_projectile, fire_blocks, False):
                fire_projectile.kill()


FIREPROJECTILE_WIDTH = 10
FIREPROJECTILE_HEIGHT = 10
FIREPROJECTILE_COLOR = "#0FFFA7"


class Projectiles(sprite.Sprite):
    def __init__(self, x, y, speed):
        sprite.Sprite.__init__(self)
        self.image = Surface((FIREPROJECTILE_WIDTH, FIREPROJECTILE_HEIGHT))
        self.image = image.load("%s/sprites/blocks/fireball.png" % ICON_DIR)
        # self.image.fill(Color(FIREPROJECTILE_COLOR))
        self.rect = Rect(x, y, FIREPROJECTILE_WIDTH, FIREPROJECTILE_HEIGHT)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed


class Trap(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        # self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/sprites/blocks/lava.png" % ICON_DIR)
        # self.image.set_colorkey(Color('#FFFFFF'))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def update(self, player, screen) -> bool:
        if pygame.sprite.collide_rect(self, player):
            return True

