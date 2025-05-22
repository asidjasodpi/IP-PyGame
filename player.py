import pygame
from settings import *
def update(self, enemies):
        keys = pygame.key.get_pressed()
 
        # Горизонтальное движение
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
 
        # Прыжок
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -self.jump_power
 
        # Гравитация
        self.velocity_y += 0.8
        dy = self.velocity_y
 
        self.is_jumping = True
        steps = int(abs(dy)) + 1
        for _ in range(steps):
            self.rect.y += dy / steps
 
            # Проверка столкновения с платформами
            for platform in self.platforms:
                if self.rect.colliderect(platform.rect):
                    if dy > 0 and self.rect.bottom <= platform.rect.top + 10:
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.is_jumping = False
                    elif dy < 0 and self.rect.top >= platform.rect.bottom - 10:
                        self.rect.top = platform.rect.bottom
                        self.velocity_y = 0
                    break  # Выходим после столкновения с одной платформой
 
            # Проверка столкновения с врагами (сверху)
            for enemy in enemies:
                if (self.rect.colliderect(enemy.rect) and
                    self.velocity_y >= 0 and
                    self.rect.bottom <= enemy.rect.top + 10):
                    enemy.kill()
                    self.score += 10
                    self.velocity_y = -12  # Отскок после убийства врага
                    break