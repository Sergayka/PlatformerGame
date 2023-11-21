#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from Player import *
from Blocks import *
"""
Попробовать реализовать блок (слизь, паутина и т.д), 
суть которой уменьшать мувспид и прыжок в n раз
"""


WIN_WIDTH = 1500  # Ширина создаваемого окна
WIN_HEIGHT = 790  # Высота

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную

BACKGROUND_COLOR = "#C0C0C0"


# TODO: Как вариант, может накатить фон в виде изображение их посвапать или вовосе убрать и уже играться с цветами
def main(game_over):
    pygame.init()  # Инициация PyGame, обязательная строчка

    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Nice game bro")  # Пишем в шапку

    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    hero = Player(55, 55)  # создаем героя по (x, y) координатам

    left = right = False  # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты

    platforms = pygame.sprite.Group()

    coins = pygame.sprite.Group()  # Группа для хранения монеток

    fire_blocks = pygame.sprite.Group()  # Группа для хранения блоков с огнем

    traps = pygame.sprite.Group()

    entities.add(hero)

    level = [
        "------------------------------------------------------------------------------------------------------------",
        "-      0                                                                                                   -",
        "-      1                --                                                                                 -",
        "                000000000                                                                                  -",
        "             --                             1                                                              -",
        "-                                                                                                          -",
        "-------   0000000                                                                                          -",
        "-         -------    0                                                                                     -",
        "-                   ----     ---                                                                           -",
        "-                                                                                                          -",
        "--                000000000000000                                                                          -",
        "--------    0     ---------------                                                                          -",
        "-                            ---   -----  000000000000                                                     -",
        "-                                         ------------                                                     -",
        "-           ---1                                                                                           -",
        "-                                                        -----                            00000000000000000-",
        "-           -----                                                                         ------------------",
        "-   -----           ----                                          -----------                              -",
        "-                                                                             --------                     -",
        "-                         -                                                                                -",
        "-                            --                                                                            -",
        "-            ---                                                                                           -",
        "-                                                                                                          -",
        "-                                                                                                          -",
        "-                                                                                                          -",
        "------------------------------------------------------------------------------------------------------------"]

    timer = pygame.time.Clock()

    x = y = 0  # координаты

    for row in level:  # вся строка
        for col in row:  # каждый символ

            if col == "-":
                platform = Platform(x, y)   #Подтягиваем платформы из файла Blocks.py
                entities.add(platform)
                platforms.add(platform)

            elif col == "0":
                coin = Coin(x, y)   #Подтягиваем монеты из файла Blocks.py
                entities.add(coin)
                coins.add(coin)

            elif col == "1":
                fire_block = ShootingBlock(x, y)    #Подтягиваем платформы из файла Blocks.py
                entities.add(fire_block)
                fire_blocks.add(fire_block)

            elif col == '*':
                trap = Trap(x, y)     #Подтягиваем шипы из файла Blocks.py
                entities.add(trap)
                traps.add(trap)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    score = 0

    while not game_over:  # Обрабатываются все события до тех пор, пока игра идет
        timer.tick(60)
        for e in pygame.event.get():  # Обрабатываем события

            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
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

        camera.update(hero)  # централизируем камеру относительно персонажа

        hero.update(left, right, up, platforms, fire_blocks)  # передвижение героя с учетом всех элементов

        for e in entities:
            screen.blit(e.image, camera.apply(e))

        collected_coins = pygame.sprite.spritecollide(hero, coins, True)    #Считываем подбор монеты

        score += len(collected_coins)   #Счетчик

        coins.update(hero)

        for fire_block in fire_blocks:
            game_over = fire_block.update(hero, platforms, traps, fire_blocks) #todo: подхватить другим методом можно мб
            screen.blit(fire_block.image, camera.apply(fire_block))

            if game_over:
                game_end(screen)

            for fire_projectile in fire_block.fire_projectiles:
                screen.blit(fire_projectile.image, camera.apply(fire_projectile))
                fire_projectile.update()

        for trap in traps:
            game_over = trap.update(hero, screen)

            if game_over:
                game_end(screen)

        # fontt = pygame.font.Font('Inter.ttf', 36)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
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


def game_end(screen):
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2 - 50))

    font = pygame.font.Font(None, 36)
    restart_text = font.render("Press R to restart or Q to quit", True, (255, 255, 255))
    screen.blit(restart_text, (WIN_WIDTH // 2 - 200, WIN_HEIGHT // 2 + 50))

    pygame.display.update()

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit("1")
            elif e.type == KEYDOWN:
                if e.key == K_r:
                    return main(False)
                elif e.key == K_q:
                    raise SystemExit('Thx for play')


if __name__ == "__main__":
    main(False)
