#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pygame import *

import pyganim
import os
from PIL import Image

ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами
# Batman, GraveRobber, Mario, SteamMan, WTFguy
ANIMATION_RIGHT = [('%s/sprites/hero/Mario/right_1.png' % ICON_DIR),
                   ('%s/sprites/hero/Mario/right_2.png' % ICON_DIR),
                   ('%s/sprites/hero/Mario/right_3.png' % ICON_DIR),
                   ('%s/sprites/hero/Mario/right_4.png' % ICON_DIR),
                   ('%s/sprites/hero/Mario/right_5.png' % ICON_DIR)]

ANIMATION_LEFT = [('%s/sprites/hero/Mario/left_1.png' % ICON_DIR),
                  ('%s/sprites/hero/Mario/left_2.png' % ICON_DIR),
                  ('%s/sprites/hero/Mario/left_3.png' % ICON_DIR),
                  ('%s/sprites/hero/Mario/left_4.png' % ICON_DIR),
                  ('%s/sprites/hero/Mario/left_5.png' % ICON_DIR)]

ANIMATION_JUMP_LEFT = [('%s/sprites/hero/Mario/jump_left.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/sprites/hero/Mario/jump_right.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/sprites/hero/Mario/jump.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/sprites/hero/Mario/default.png' % ICON_DIR, 0.1)]






























im = Image.open(ANIMATION_STAY[0][0])
(width, height) = im.size


MOVE_SPEED = 3

WIDTH = width

HEIGHT = height

COLOR = "#888888"

JUMP_POWER = 10

GRAVITY = 0.35  # Сила, которая будет тянуть нас вниз

ANIMATION_DELAY = 0.1  # скорость смены кадров


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

    def update(self, left, right, up, platforms, fire_blocks):

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

        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, fire_blocks)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms, fire_blocks)

    def collide(self, xvel, yvel, platforms, fire_blocks):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                self.handle_collision(xvel, yvel, p)

        for p in fire_blocks:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком
                self.handle_collision(xvel, yvel, p)

    def handle_collision(self, xvel, yvel, p):
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
