import pygame
pygame.init()
pygame.mixer.init()
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 980
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


BACK_BLUE = (12, 20, 66)
LIGHTBLUE = (122, 206, 230)
PINK = (234, 130, 223)
PRETT_RED = (255, 116, 135)
FIOL = (125, 16, 162)
# Игрок
PLAYER_SPEED = 10
PLAYER_JUMP_POWER = 19
PLAYER_HEALTH = 1000
# Враги
ENEMY_SPEED = 4
WAVE_DELAY = 5000  # 5 сек между волнами