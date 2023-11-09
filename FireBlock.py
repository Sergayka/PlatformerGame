# # import pygame.sprite
# # from pygame import *
# # import os
# #
# # from FireProjectile import *
# #
# # ICON_DIR = os.path.dirname(__file__)
# #
# # FIREBLOCK_WIDTH = 32
# # FIREBLOCK_HEIGHT = 32
# #
# # FIREBLOCK_COLOR = "#DAA520"
# #
# #
# # class FireBlock(sprite.Sprite):
# #     def __init__(self, x, y):
# #         sprite.Sprite.__init__(self)
# #         self.image = Surface((FIREBLOCK_WIDTH, FIREBLOCK_HEIGHT))
# #         self.image.fill(Color(FIREBLOCK_COLOR))
# #         # self.image = image.load("%s/sprites/fireblock/fireblock.png" % ICON_DIR)
# #         self.rect = Rect(x, y, FIREBLOCK_WIDTH, FIREBLOCK_HEIGHT)
# #
# #         self.projectiles = sprite.Group()
# #         self.move_speed = 5
# #         self.direction = 1
# #
# #         self.shoot_timer = 0
# #         self.shoot_delay = 60
# #
# #     def update(self, hero):
# #             # Обновление движения огненного блока
# #             self.rect.x += self.move_speed * self.direction
# #
# #             # Логика изменения направления при достижении границы
# #             if self.rect.right > FIREBLOCK_WIDTH or self.rect.left < 0:
# #                 self.direction *= -1
# #
# #             # Логика стрельбы снарядами
# #             self.shoot_timer += 1
# #             if self.shoot_timer >= self.shoot_delay:
# #                 self.shoot_projectiles()
# #                 self.shoot_timer = 0
# #
# #             # Обновление положения снарядов
# #             self.projectiles.update()
# #
# #             # Очистка снарядов, которые вышли за пределы экрана
# #             for projectile in self.projectiles.copy():
# #                 if projectile.rect.right < 0 or projectile.rect.left > FIREBLOCK_WIDTH:
# #                     self.projectiles.remove(projectile)
# #
# #     def shoot_projectiles(self):
# #         # Логика стрельбы снарядами
# #         projectile = FireProjectile(self.rect.x, self.rect.y)
# #         self.projectiles.add(projectile)
# #
# #     def spawn_projectile(self):
# #         projectile = FireProjectile(self.rect.x, self.rect.y)
# #         self.projectiles.add(projectile)
# #
# #     def draw_projectileS(self, screen):
# #         self.projectiles.draw(screen)
#
#
# import pygame.sprite
# from pygame import *
# import os
#
# ICON_DIR = os.path.dirname(__file__)
#
# FIREBLOCK_WIDTH = 32
# FIREBLOCK_HEIGHT = 32
#
# FIREBLOCK_COLOR = "#DAA520"
#
#
# class FireBlock(sprite.Sprite):
#     def __init__(self, x, y):
#         sprite.Sprite.__init__(self)
#         self.image = Surface((FIREBLOCK_WIDTH, FIREBLOCK_HEIGHT))
#         # self.image = image.load("%s/sprites/blocks/fireblock.png" % ICON_DIR)
#         self.image.fill(Color(FIREBLOCK_COLOR))
#         self.rect = Rect(x, y, FIREBLOCK_WIDTH, FIREBLOCK_HEIGHT)
#
#     def update(self, Player):
#         if pygame.sprite.collide_rect(self, Player):
#             raise SystemExit('gg')
