import pygame
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_range=(0, SCREEN_WIDTH)):
        super().__init__()
        
        self.image = pygame.Surface((30, 30))
        self.image.fill(PRETT_RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = ENEMY_SPEED

        self.direction = 1  # Движение влево
        self.patrol_start, self.patrol_end = patrol_range

        self.stunned = False         # Признак оглушения
        self.stunned_start_time = 0  # Время начала оглушения
        self.stun_duration = 500     # Длительность в миллисекундах (0.5 секунды)
    
    def bounce(self, player_x):
        if not self.stunned:
            if self.rect.centerx < player_x:
                self.rect.x -= 30
            else:
                self.rect.x += 30
            self.stunned = True
            self.stunned_start_time = pygame.time.get_ticks()

    def update(self):
        if self.stunned:
            if pygame.time.get_ticks() - self.stunned_start_time >= self.stun_duration:
                self.stunned = False
            return  # ничего не делает, пока оглушён
        self.rect.x += self.speed * self.direction
        # Меняем направление, если достиг границы патрулирования
        if self.rect.left < self.patrol_start or self.rect.right > self.patrol_end:
            self.direction *= -1

class WaveSystem:
    def __init__(self, platforms):
        self.is_waiting = False       # ждём ли начала новой волны
        self.wait_start_time = 0
        self.wave = 0
        self.max_waves = 3
        self.enemies = pygame.sprite.Group()
        self.last_wave_time = 0
        self.platforms = platforms

        self.stars = pygame.sprite.Group()
        self.colected_stars = 0
        

    def spawn_wave(self):
        
        self.wave += 1
        self.enemies.empty()  # очистка прошлых врагов
        self.stars.empty()
        if self.wave == 1:
            # Один враг на платформе
            self._spawn_on_platform(7)
            self._spawn_on_platform(8)

        elif self.wave == 2:
            # Один на земле, два на платформах
            self._spawn_on_ground(2)
            self._spawn_on_platform(4)
            self._spawn_on_platform(5)

        elif self.wave == 3:
            # Два на земле, три на платформах
            self._spawn_on_ground(2)
            self._spawn_on_platform(4)
            self._spawn_on_platform(5)
            self._spawn_on_platform(6)
            self._spawn_on_platform(7)
            self._spawn_on_platform(8)



        self.last_wave_time = pygame.time.get_ticks()
        self.is_waiting = False

    def _spawn_on_ground(self, count):
        position = [
            100, SCREEN_WIDTH - 100
        ]

        for pos in position:
            enemy = Enemy(pos, SCREEN_HEIGHT - 50)
            self.enemies.add(enemy)


    def _spawn_on_platform(self, index,):

        if index < len(self.platforms.sprites()):
            platform = list(self.platforms)[index]
            x = platform.rect.x + platform.rect.width // 2
            y = platform.rect.y - 30
            enemy = Enemy(x, y, patrol_range=(platform.rect.left, platform.rect.right))
            self.enemies.add(enemy)


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