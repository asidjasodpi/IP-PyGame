import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, platforms):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PLAYER_SPEED
        self.jump_power = PLAYER_JUMP_POWER
        self.health = PLAYER_HEALTH
        self.score = 0
        self.is_jumping = False
        self.velocity_y = 0
        self.platforms = platforms  # Теперь игрок знает о платформах
        
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

        # Проверка столкновений по вертикали
        self.rect.y += dy
        self.is_jumping = True

        for platform in self.platforms:
            if self.rect.colliderect(platform.rect):
                if dy > 0 and self.rect.bottom <= platform.rect.top + 10:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.is_jumping = False
        # Проверка прыжка на врагов
        for enemy in enemies:
            if (self.rect.colliderect(enemy.rect) and
                self.velocity_y >= 0 and
                self.rect.bottom <= enemy.rect.top + 5):
                enemy.kill()
                self.score += 10
                self.velocity_y = -5  # Отскок

                
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return "game_over"
        return "game"