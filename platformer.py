#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
from Player import *
from Blocks import *
from Coin import *

"""
Можем изменить размер нашего приложения (но не особо рекомендую), придется тогда менять все наши блоки
(подстраивать под размер) строки 15-16, так же можно поиграться с бэком, строка 20
В строке 27 можем изменить название нашей игры на фио, к примеру, строить самостоятельно (ИГРА ДОБРАТЬСЯ ИЗ ТОЧКИ А В ТОЧКУ Б)

строки 13, 15, 17, 19, 25, 39-67, 84-107
"""

WIN_WIDTH = 1080  # Ширина создаваемого окна
WIN_HEIGHT = 700  # Высота

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную

BACKGROUND_COLOR = "#CC99FF"

# TODO: Как вариант, может накатить фон в виде изображение их посвапать или вовосе убрать и уже играться с цветами
def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("test")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    coin = Coin(100, 100)
    coin_group = pygame.sprite.Group()
    coin_group.add(coin)

    hero = Player(55, 55)  # создаем героя по (x, y) координатам
    left = right = False  # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться

    entities.add(hero)
    entities.add(coin)

    level = [
        "----------------------------------",
        "-                                -",
        "-                       --       -",
        "-                                -",
        "-            --                  -",
        "-                                -",
        "-------                          -",
        "-                                -",
        "-                   ----     --- -",
        "-                                -",
        "--                               -",
        "--------------    ----------------",
        "-                            --- -",
        "-                                -",
        "-                                -",
        "-      ---                       -",
        "-                                -",
        "-   -------         ----         -",
        "-                                -",
        "-                         -      -",
        "-                            --  -",
        "-                                -",
        "-                                -",
        "----------------------------------"]

    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while True:
        timer.tick(60)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, platforms)  # передвижение
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        coin_group.update(hero)
        coin_group.draw(screen)

        pygame.display.update()  # обновление и вывод всех изменений на экран


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


if __name__ == "__main__":
    main()