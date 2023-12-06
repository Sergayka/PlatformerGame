#!/usr/bin/env python
# -*- coding: utf-8 -*-

from platformer import *
import pygame.sprite
from pygame import *
import os

# region Platform block
PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
# PLATFORM_COLOR = "#FFFFFF"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        # self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/sprites/blocks/random_blocks/stone_bricks1.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


# endregion

# region Coin
COIN_WIDTH = 30
COIN_HEIGHT = 30
COIN_COLOR = "#DAA520"
COLOR = "#FFFFFF"


class Coin(sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Surface((COIN_WIDTH, COIN_HEIGHT))
        self.image.fill(Color(COIN_COLOR))

        self.image = image.load("%s/sprites/coin/coin3.png" % ICON_DIR)

        self.image.set_colorkey(Color(COLOR))
        self.rect = Rect(x, y, COIN_WIDTH, COIN_HEIGHT)

    def update(self, player):
        if pygame.sprite.collide_rect(self, player):
            self.kill()


# endregion

# region FireBlock

SHOOTINGBLOCK_WEIGHT = 32
SHOOTINGBLOCK_HEIGHT = 32

FIREBLOCK_COLOR = "#DAA520"


class ShootingBlock(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((SHOOTINGBLOCK_WEIGHT, SHOOTINGBLOCK_HEIGHT))
        self.image = image.load("%s/sprites/blocks/minecraft/dispencer.png" % ICON_DIR)
        # self.image.fill(Color(FIREBLOCK_COLOR))
        self.rect = Rect(x, y, SHOOTINGBLOCK_WEIGHT, SHOOTINGBLOCK_HEIGHT)

        self.projectiles = pygame.sprite.Group()
        self.create_projectiles(x, y)

        self.fire_timer = 0
        self.fire_interval = 2000

    def create_projectiles(self, x, y):
        projectile_right = Projectiles(self.rect.x + 34, self.rect.y + 9, speed=1)
        projectile_left = Projectiles(self.rect.x - 19, self.rect.y + 9, speed=-1)

        self.projectiles.add(projectile_right, projectile_left)

    def update(self, player, platforms, thorns, fire_blocks):
        current_time = pygame.time.get_ticks()
        if current_time - self.fire_timer > self.fire_interval:
            self.fire_timer = current_time
            self.create_projectiles(self.rect.x, self.rect.y)

        for projectile in self.projectiles:
            projectile.update()
            if pygame.sprite.collide_rect(projectile, player):
                return True

            if pygame.sprite.spritecollide(projectile, platforms, False) or \
                    pygame.sprite.spritecollide(projectile, thorns, False) or \
                    pygame.sprite.spritecollide(projectile, fire_blocks, False):
                projectile.kill()


# endregion

# region Projectiles
PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 10
FIREPROJECTILE_COLOR = "#0FFFA7"


class Projectiles(sprite.Sprite):
    def __init__(self, x, y, speed):
        sprite.Sprite.__init__(self)
        self.image = Surface((PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
        self.image = image.load("%s/sprites/projectiles/fireball.png" % ICON_DIR)
        # self.image.fill(Color(FIREPROJECTILE_COLOR))
        self.rect = Rect(x, y, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed


# endregion

# region Trap
class Trap(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        # self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/sprites/blocks/minecraft/lava.png" % ICON_DIR)
        # self.image.set_colorkey(Color('#FFFFFF'))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def update(self, player, screen) -> bool:
        if pygame.sprite.collide_rect(self, player):
            return True

# endregion
