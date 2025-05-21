import pygame
from settings import *
from player import Player
from enemy import Enemy, WaveSystem

class Level:
    def __init__(self, screen):
        self.screen = screen
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.setup_level()
        self.player = Player(100, SCREEN_HEIGHT - 150, self.platforms)  # Передаем платформы
        self.all_sprites.add(self.player)
        self.wave_system = WaveSystem()
        
    def setup_level(self):
        # Создаем платформы
        ground = pygame.sprite.Sprite()
        ground.image = pygame.Surface((SCREEN_WIDTH, 20))
        ground.image.fill(WHITE)
        ground.rect = ground.image.get_rect()
        ground.rect.x = 0
        ground.rect.y = SCREEN_HEIGHT - 20
        self.platforms.add(ground)
        self.all_sprites.add(ground)
        
        platform1 = pygame.sprite.Sprite()
        platform1.image = pygame.Surface((200, 20))
        platform1.image.fill(WHITE)
        platform1.rect = platform1.image.get_rect()
        platform1.rect.x = 300
        platform1.rect.y = 400
        self.platforms.add(platform1)
        self.all_sprites.add(platform1)
        
    def update(self):
        # Обновляем игрока и врагов
        self.player.update(self.wave_system.enemies)
        game_state = self.wave_system.update()
        
        # Проверка столкновений с врагами (боковой урон)
        for enemy in self.wave_system.enemies:
            if (self.player.rect.colliderect(enemy.rect) and
                self.player.velocity_y <= 0 and  # Не падает сверху
                self.player.rect.bottom > enemy.rect.centery):  # Боковое столкновение
                game_state = self.player.take_damage(10)
        
        # Отрисовка
        self.screen.fill(BLACK)
        self.all_sprites.add(*self.wave_system.enemies)
        self.all_sprites.draw(self.screen)
        
        self.wave_system.enemies.draw(self.screen)
        self.draw_hud()
        
        return game_state
    
    def draw_hud(self):
        font = pygame.font.SysFont("Arial", 24)
        health_text = font.render(f"Здоровье: {self.player.health}", True, WHITE)
        score_text = font.render(f"Счёт: {self.player.score}", True, WHITE)
        wave_text = font.render(f"Волна: {self.wave_system.wave} из {self.wave_system.max_waves}", True, YELLOW)

        self.screen.blit(health_text, (20, 20))
        self.screen.blit(score_text, (20, 50))
        self.screen.blit(wave_text, (20, 80))