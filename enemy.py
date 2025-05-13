import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30,30))
        self.image.fill(R)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.x -= self.speed

class WaveSystem:
    def __init__(self):
        self.wave = 0
        self.max_waves = 5
        self.enemies = pygame.sprite.Group()
        self.last_wave_time = 0

    def spawn_wave(self):
        if pygame.time.get_ticks() - self.last_wave_time > WAVE_DELAY:
            self.wave += 1
            for i in range(3 + self.wave * 2):
                enemy = Enemy(WIDTH, HEIGHT - 50)
                self.enemies.add(enemy)
            self.last_wave_time = pygame.time.get_ticks()

    def update(self):
        if self.wave < self.max_waves:
            self.spawn_wave()
        elif len(self.enemies) == 0:
            return "win" 
        return "game"