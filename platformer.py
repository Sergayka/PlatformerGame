#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from Player import *
from Blocks import *


WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 500  # Высота

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную

BACKGROUND_COLOR = "#C0C0C0"


def main(game_over):
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Game")  # Пишем в шапку

    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    hero = Player(55, 55)  # создаем героя по (x, y) координатам

    left = right = False  # по умолчанию - стоим
    up = False

    entities = pygame.sprite.Group()  # Все объекты

    platforms = pygame.sprite.Group()

    coins = pygame.sprite.Group()  # Группа для хранения монеток

    shooting_blocks = pygame.sprite.Group()  # Группа для хранения блоков с огнем

    traps = pygame.sprite.Group()

    entities.add(hero)

    level = [
        "------------------------------------------------------------------------------------------------------------",
        "-                                                                                                          -",
        "-                       --                                                                                 -",
        "-                                                                                                          -",
        "-            --                                                                                            -",
        "-                                                                     1                                    -",
        "-------   0000000                                                                                          -",
        "-       ---------                                                                                          -",
        "-                   ----     ---                                                                           -",
        "-                                                                                                          -",
        "--                                                                                                         -",
        "--------          ---------------                                                                          -",
        "-                            ---   -----                                                                   -",
        "-                                         ------------                                                     -",
        "-           ---1                                                                                           -",
        "-                                                        -----                                             -",
        "-           -----                                                                         ------------------",
        "-   -----           ----                                          -----------                              -",
        "-                                                                             --------                     -",
        "-                         -                                                                                -",
        "-                            --                                                                            -",
        "-            ---                                                                                           -",
        "-                                                                                                          -",
        "-****************************00000*************************************************************************-",
        "------------------------------------------------------------------------------------------------------------"]

    timer = pygame.time.Clock()

    x = y = 0  # координаты

    for row in level:  # вся строка
        for col in row:  # каждый символ

            if col == "-":
                platform = Platform(x, y)  # Подтягиваем платформы из файла Blocks.py
                entities.add(platform)
                platforms.add(platform)

            elif col == "0":
                coin = Coin(x, y)  # Подтягиваем монеты из файла Blocks.py
                entities.add(coin)
                coins.add(coin)

            elif col == "1":
                shooting_block = ShootingBlock(x, y)  # Подтягиваем платформы из файла Blocks.py
                entities.add(shooting_block)
                shooting_blocks.add(shooting_block)

            elif col == '*':
                trap = Trap(x, y)  # Подтягиваем шипы из файла Blocks.py
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

        hero.update(left, right, up, platforms, shooting_blocks)  # передвижение героя с учетом всех элементов

        for e in entities:
            screen.blit(e.image, camera.apply(e))

        collected_coins = pygame.sprite.spritecollide(hero, coins, True)  # Считываем подбор монеты

        score += len(collected_coins)  # Счетчик
        print(screen, type(screen))
        coins.update(hero)

        if is_win(score, level):
            _font = pygame.font.Font('fonts/GameOver.ttf', 64)
            score_text = _font.render("YOU WON!", True, (255, 255, 255))
            screen.blit(score_text, (WIN_WIDTH // 2, WIN_HEIGHT // 2))
            screen.blit(pygame.image.load("%s/sprites/background/gobg2.png" % ICON_DIR), (0, 0))
            game_win_end(screen)

        for shooting_block in shooting_blocks:
            game_over = shooting_block.update(hero, platforms, traps,
                                              shooting_blocks)  # todo: подхватить другим методом можно мб
            screen.blit(shooting_block.image, camera.apply(shooting_block))

            if game_over:
                game_end(screen)

            for projectile in shooting_block.projectiles:
                screen.blit(projectile.image, camera.apply(projectile))
                projectile.update()

        for trap in traps:
            game_over = trap.update(hero, screen)

            if game_over:
                game_end(screen)

        _font = pygame.font.Font(None, 36)
        score_text = _font.render(f"Score: {score}", True, (255, 255, 255))
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
    bg = pygame.image.load("sprites/background/gobg.png")
    screen.blit(bg, (0, 0))
    font = pygame.font.Font("fonts/Atari.ttf", 68)
    game_text = font.render("GAME", True, (255, 255, 255))
    screen.blit(game_text, (WIN_WIDTH // 2 - 130, WIN_HEIGHT // 2 - 150))
    over_text = font.render("OVER", True, (255, 255, 255))
    screen.blit(over_text, (WIN_WIDTH // 2 - 130, WIN_HEIGHT // 2 - 75))

    font = pygame.font.Font(None, 36)
    restart_text = font.render("Press R to restart or Q to quit", True, (255, 255, 255))
    screen.blit(restart_text, (WIN_WIDTH // 2 - 160, WIN_HEIGHT // 2 + 50))

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


def is_win(score: int, level: list) -> bool:
    win_score = 0
    for s in level:
        win_score += s.count('0')

    return win_score == score


# TODO: create a function to show ararat in case of equality of score and the amount of coins at the level
def game_win_end(screen) -> None:
    bg = pygame.image.load("%s/sprites/background/ararat.png" % ICON_DIR)
    screen.blit(bg, (0, 0))
    stay_img = pygame.image.load(ANIMATION_STAY[0][0])
    screen.blit(stay_img, (WIN_WIDTH // 2 - 235, WIN_HEIGHT // 2 + 25))
    screen.blit(stay_img, (WIN_WIDTH // 2 + 220, WIN_HEIGHT // 2 - 90))
    _font = pygame.font.Font("fonts/GameOver.ttf", 68)
    game_text = _font.render("YOU WIN!", True, (255, 255, 255))
    screen.blit(game_text, (WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2 - 170))

    _font = pygame.font.Font(None, 36)
    restart_text = _font.render("Press R to restart or Q to quit", True, (255, 255, 255))
    screen.blit(restart_text, (WIN_WIDTH // 2 - 160, WIN_HEIGHT // 2 + 100))

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
