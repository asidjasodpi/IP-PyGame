#
# #Импорт
import pygame
import sys

# #Окно
WIDTH = 1280
HEIGHT = 720
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PyProject')
pygame.display.set_icon(pygame.image.load("logo.jpg"))
bg = pygame.image.load('Test_map.png')
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
clock = pygame.time.Clock()
# Классы
#-------------
PLAYER_SPEED = 5
GRAVITY = 0.5
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)  # Хитбокс
        self.vel_y = 0  # Скорость падения
        self.on_ground = False  # Стоит ли на платформе

    def move(self, keys):
        # Горизонтальное движение
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += PLAYER_SPEED

        # Прыжок
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -10  # Прыжок вверх

    def apply_gravity(self, platforms):
        self.vel_y += GRAVITY  # Притяжение вниз
        self.rect.y += self.vel_y  # Двигаем игрока вниз

        # Проверка коллизии с платформами
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True


class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)  # Хитбокс
        self.direction = 1  # Направление движения (1 = вправо, -1 = влево)
        self.speed = 2  # Скорость движения
        self.vel_y = 0  # Скорость падения
        self.on_ground = False  # Стоит ли на платформе

    def update(self):
        self.rect.x += self.speed * self.direction

        # Меняем направление при достижении границы
        if self.rect.x <= 0 or self.rect.x >= WIDTH - self.rect.width:
            self.direction *= -1

    def apply_gravity(self, platforms):
        self.vel_y += GRAVITY  # Притяжение вниз
        self.rect.y += self.vel_y  # Двигаем игрока вниз

        # Проверка коллизии с платформами
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)  # Хитбокс платформы

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 200, 200), self.rect)  # Светло-серый цвет
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)  # Чёрная рамка 

player = Player(100, 400)
enemies = [Enemy(300, 500), Enemy(600, 500)]
platforms = [
    Platform(100, 500, 150, 20),
    Platform(400, 450, 200, 20),
    Platform(650, 350, 100, 20),
    Platform(0, 600, 1280, 20)
]

# #Игровой цикл
running = True
while running:
    window.fill((0, 0, 0))  # Очистка экрана      ?????
    clock.tick(60)
    window.blit(bg,(0,0))
#     pygame.display.update()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

    # Отрисовка платформ
    for platform in platforms:
        platform.draw(window)

    # Отрисовка игрока
    pygame.draw.rect(window, (0, 255, 0), player.rect)

    # Отрисовка врагов
    for enemy in enemies:
        pygame.draw.rect(window, (255, 0, 0), enemy.rect)
        enemy.update()
        enemy.apply_gravity(platforms)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление игроком
    keys = pygame.key.get_pressed()
    player.move(keys)
    player.apply_gravity(platforms)

    pygame.display.flip()
#Завершение работы программы
sys.exit()
pygame.quit()
