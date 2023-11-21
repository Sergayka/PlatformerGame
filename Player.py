#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame.sprite
from pygame import *

import pyganim
import os

"""
Мы смело можем поиграться со скоростью, гравитаций, силой прижка и т.д (строчки 14 - 28)
"""

MOVE_SPEED = 3

WIDTH = 21

HEIGHT = 35

COLOR = "#888888"

JUMP_POWER = 10

GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз

ANIMATION_DELAY = 0.1  # скорость смены кадров

ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

# Список персонажей: Mario, WTFguy, GraveRobber (не готов), Batman, WoodCutter (не готов), SteamMan(не готов)

ANIMATION_RIGHT = [('%s/sprites/hero/WTFguy/right_1.png' % ICON_DIR),
                   ('%s/sprites/hero/WTFguy/right_2.png' % ICON_DIR),
                   ('%s/sprites/hero/WTFguy/right_3.png' % ICON_DIR),
                   ('%s/sprites/hero/WTFguy/right_4.png' % ICON_DIR),
                   ('%s/sprites/hero/WTFguy/right_5.png' % ICON_DIR)]
# ANIMATION_RIGHT = [('%s/sprites/player/Mario/guy.png' % ICON_DIR),
#                    ('%s/sprites/player/Mario/guy.png' % ICON_DIR),
#                    ('%s/sprites/player/Mario/guy.png' % ICON_DIR),
#                    ('%s/sprites/player/Mario/guy.png' % ICON_DIR),
#                    ('%s/sprites/player/Mario/guy.png' % ICON_DIR)]

ANIMATION_LEFT = [('%s/sprites/hero/WTFguy/left_1.png' % ICON_DIR),
                  ('%s/sprites/hero/WTFguy/left_2.png' % ICON_DIR),
                  ('%s/sprites/hero/WTFguy/left_3.png' % ICON_DIR),
                  ('%s/sprites/hero/WTFguy/left_4.png' % ICON_DIR),
                  ('%s/sprites/hero/WTFguy/left_5.png' % ICON_DIR)]

# ANIMATION_LEFT = [('%s/sprites/player/Mario/guy.png' % ICON_DIR),
#                   ('%s/sprites/player/Mario/guy.png' % ICON_DIR),
#                   ('%s/sprites/player/Mario/guy.png' % ICON_DIR),
#                   ('%s/sprites/player/Mario/guy.png' % ICON_DIR),
#                   ('%s/sprites/player/Mario/guy.png' % ICON_DIR)]

ANIMATION_JUMP_LEFT = [('%s/sprites/hero/WTFguy/jump_left.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/sprites/hero/WTFguy/jump_right.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/sprites/hero/WTFguy/jump.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/sprites/hero/WTFguy/default.png' % ICON_DIR, 0.1)]

# ANIMATION_JUMP_LEFT = [('%s/sprites/player/Mario/guy.png' % ICON_DIR, 0.1)]
# ANIMATION_JUMP_RIGHT = [('%s/sprites/player/Mario/guy.png' % ICON_DIR, 0.1)]
# ANIMATION_JUMP = [('%s/sprites/player/Mario/guy.png' % ICON_DIR, 0.1)]
# ANIMATION_STAY = [('%s/sprites/player/Mario/guy.png' % ICON_DIR, 0.1)]


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        #        Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        #        Анимация движения влево
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

    def update(self, left, right, up, platforms):

        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image.fill(Color(COLOR))
            if up:  # для прыжка влево есть отдельная анимация
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image.fill(Color(COLOR))
            if up:
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
            if not up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))

        if not self.onGround:
            self.yvel += GRAVITY

        # if pygame.sprite.collide_rect(self, Coin):
        #     self.kill()

        self.onGround = False;  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.yvel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0  # и энергия прыжка пропадает
