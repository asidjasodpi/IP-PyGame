import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, platforms):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(FIOL)
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

        self.last_hit_time = 0
        self.invincibility_delay = 500  # в миллисекундах
        
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

                    enemy_dead = pygame.mixer.Sound('music/enemy_dead.ogg')
                    enemy_dead.play()

                    self.score += 10
                    self.velocity_y = -12  # Отскок после убийства врага
                    break

                
    def take_damage(self, damage, enemy_x):
        now = pygame.time.get_ticks()
        if now - self.last_hit_time < self.invincibility_delay:
            return "game"  # временно неуязвим

        self.last_hit_time = now
        self.health -= damage

        player_kick = pygame.mixer.Sound('music/player_kick.ogg')
        player_kick.play()

        # Отскок: если враг справа — отскочить влево, и наоборот
        if self.rect.centerx < enemy_x:
            self.rect.x -= 30
        else:
            self.rect.x += 30
        self.velocity_y = -10  # подпрыгнуть вверх немного

        
        if self.health <= 0:
            player_dead = pygame.mixer.Sound('music/player_dead.ogg')
            player_dead.play()
            return "game_over"
        return "game"