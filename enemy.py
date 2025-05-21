import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = ENEMY_SPEED
        self.direction = -1  # Движение влево
        
    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH + 1000:
            self.kill()  # Удаляем врагов за экраном

class WaveSystem:
    def __init__(self):
        self.is_waiting = False       # ждём ли начала новой волны
        self.wait_start_time = 0
        self.wave = 0
        self.max_waves = 3
        self.enemies = pygame.sprite.Group()
        self.last_wave_time = 0
        
    def spawn_wave(self):
        
        self.wave += 1
        self.enemies.empty()  # очистка прошлых врагов
        for i in range(3 + (self.wave) * 2):  # 3, 5, 7 врагов
            x = SCREEN_WIDTH + i * 60
            enemy = Enemy(x, SCREEN_HEIGHT - 50)
            self.enemies.add(enemy)
        print(f"Спавн волны {self.wave}: {len(self.enemies)} врагов")
        self.last_wave_time = pygame.time.get_ticks()
        self.is_waiting = False
            
    def update(self):
        if self.wave >= self.max_waves and len(self.enemies) == 0:
            return "win"

        # Если враги побеждены и ещё есть волны
        if not self.is_waiting and len(self.enemies) == 0 and self.wave < self.max_waves:
            self.is_waiting = True
            self.wait_start_time = pygame.time.get_ticks()
        
        # Ждём перед следующей волной
        if self.is_waiting:
            if pygame.time.get_ticks() - self.wait_start_time >= WAVE_DELAY:
                self.spawn_wave()

        self.enemies.update()
        return "game"