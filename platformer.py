#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame

# from FireBlock import *
from Player import *
from Blocks import *
# from Coin import *

"""
Можем изменить размер нашего приложения (но не особо рекомендую), придется тогда менять все наши блоки
(подстраивать под размер) строки 15-16, так же можно поиграться с бэком, строка 20
В строке 27 можем изменить название нашей игры на фио, к примеру, строить самостоятельно (ИГРА ДОБРАТЬСЯ ИЗ ТОЧКИ А В ТОЧКУ Б)

строки 13, 15, 17, 19, 25, 39-67, 84-107
"""

WIN_WIDTH = 1000  # Ширина создаваемого окна
WIN_HEIGHT = 992  # Высота

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную

BACKGROUND_COLOR = "#C0C0C0"

# TODO: Как вариант, может накатить фон в виде изображение их посвапать или вовосе убрать и уже играться с цветами
def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Nice game bro")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    # bg = pygame.image.load("")

    hero = Player(55, 55)  # создаем героя по (x, y) координатам
    left = right = False  # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться

    coins = pygame.sprite.Group() # Группа для хранения монеток

    fire_blocks = pygame.sprite.Group() # Группа для хранения блоков с огнем

    thorns = pygame.sprite.Group()

    # fire_projectiles = pygame.sprite.Group()

    entities.add(hero)

    level = [
        "------------------------------------------------------------------------------------------------------------",
        "-      0                                                                                                   -",
        "-                       --                                                                                 -",
        "-                                                                                                          -",
        "-            --                                                                                            -",
        "-   00                                                                                                     -",
        "-------   0000000                                                                                          -",
        "-         -------    0                                                                                     -",
        "-                   ----     ---                                                                           -",
        "-                                                                                                          -",
        "--                000000000000000                                                                          -",
        "--------    0     ---------------                                                                          -",
        "-                            ---   -----  000000000000                                                     -",
        "-                                         ------------                                                     -",
        "-              1                                                                                           -",
        "-                                                        -----                            00000000000000000-",
        "-                                                                                         ------------------",
        "-   -----           ----                                          -----------                              -",
        "-                                                                             --------                     -",
        "-                         -                                                                                -",
        "-                            --                                                                            -",
        "-            ---                                                                                           -",
        "-                                                                                                          -",
        "-                                                                                                          -",
        "-                                                                                                          -",
        "-**********************************************************************************************************-",
        "-**********************************************************************************************************-",
        "-**********************************************************************************************************-",
        "-**********************************************************************************************************-",
        "-**********************************************************************************************************-",
        "------------------------------------------------------------------------------------------------------------"]

    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)

            elif col == "0":
                coin = Coin(x, y)
                entities.add(coin)
                coins.add(coin)

            elif col == "1":
                fire_block = FireBlock(x, y)
                entities.add(fire_block)
                fire_blocks.add(fire_block)

            elif col == '*':
                th = Thorn(x, y)
                entities.add(th)
                thorns.add(th)


            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    score = 0

    while True:
        timer.tick(60)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and (e.key == K_UP or e.key == K_SPACE):
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and (e.key == K_UP or e.key == K_SPACE):
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


        # hero.update(left, right, up, platforms)
        collected_coins = pygame.sprite.spritecollide(hero, coins, True)
        score += len(collected_coins)

        # coins.draw(screen) #
        coins.update(hero)

        for fire_block in fire_blocks:
            fire_block.update(hero)


            screen.blit(fire_block.image, camera.apply(fire_block))
            for fire_projectile in fire_block.fire_projectiles:
                screen.blit(fire_projectile.image, camera.apply(fire_projectile))
                fire_projectile.update()
            # fire_block.fire_projectiles.draw(screen)
            # fire_block.fire_projectiles.update()
            # fire_block.fire_projectiles.update()
        # TODO: for fire_block in fire_blocks:
            # fire_block.fire_projectiles.draw(screen)
            # TODO: fire_block.fire_projectiles.update()
            # fire_block.fire_projectiles.draw(screen)

        # TODO: for fire_block in fire_blocks:
        #     TODO: fire_block.fire_projectiles.draw(screen)
            # fire_block.fire_projectiles.draw(screen)
            # fire_block.update(hero)


        # fire_blocks.draw(screen)

        # for fire_block in fire_blocks:
        #     fire_block.fire_projectiles.update()
        # fire_blocks.update(hero)
        # fire_blocks.draw(screen)
        #
        # for fire_block in fire_blocks:
        #     if pygame.sprite.spritecollide(hero, fire_block.pro, True):
        #         raise SystemExit('gg')

        # FireBlock.dra
        # FireBlock.draw_fire(screen)
        # fire_blocks.draw(screen)

        # for fire_block in fire_blocks:
        #     if sprite.spritecollide(hero, FireBlock.shoots)

        thorns.update(hero)

        # fontt = pygame.font.Font('Inter.ttf', 36)

        fontt = pygame.font.Font(None, 36)
        score_text = fontt.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (WIN_WIDTH - 175, 20))

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
