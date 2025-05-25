import pygame
from settings import *
from player import Player
from enemy import WaveSystem


class Level:
    def __init__(self, screen):
        self.screen = screen
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.setup_level()
        self.player = Player(100, SCREEN_HEIGHT - 150, self.platforms)  # Передаем платформы
        self.all_sprites.add(self.player)
        self.wave_system = WaveSystem(self.platforms)

        
        
    def setup_level(self):
        ground = pygame.sprite.Sprite()
        ground.image = pygame.Surface((SCREEN_WIDTH, 20))
        ground.image.fill(WHITE)
        ground.rect = ground.image.get_rect(topleft=(0, SCREEN_HEIGHT - 20))
        self.platforms.add(ground)
        self.all_sprites.add(ground)

        # Список платформ: (x, y, width, height, NAME
        platform_data = [
            (SCREEN_WIDTH //2 - 250, 200, 500, 33, 'image/platform1_l.jpg'),

            (80, 350, 250, 33, 'image/platform2.jpg'),
            (SCREEN_WIDTH - 330, 350, 250, 33, 'image/platform1.jpg'),

            (450, 480, 198, 33, 'image/platform1.jpg'),
            (SCREEN_WIDTH - 648, 480, 198, 33, 'image/platform2.jpg'),

            (SCREEN_WIDTH //2 - 250, 660, 500, 33, 'image/platform2_l.jpg'),

            (150, 820, 500, 33, 'image/platform3.jpg'),
            (SCREEN_WIDTH - 650, 820, 500, 33, 'image/platform4.jpg'),

        ]

        for x, y, w, h, platform_name in platform_data:
            platform = pygame.sprite.Sprite()
            platform.image = pygame.transform.scale(pygame.image.load(platform_name), (w, h)) 
            platform.rect = platform.image.get_rect(topleft=(x, y))
            self.platforms.add(platform)
            self.all_sprites.add(platform)
        
    def update(self):
        # Обновляем игрока и врагов
        self.player.update(self.wave_system.enemies)
        game_state = self.wave_system.update()
        self.wave_system.stars.draw(self.screen)
        
        # Проверка столкновений с врагами (боковой урон)
        for enemy in self.wave_system.enemies:
            if (self.player.rect.colliderect(enemy.rect) and
                self.player.velocity_y <= 0 and  # Не падает сверху
                self.player.rect.bottom > enemy.rect.centery):  # Боковое столкновение
                enemy.bounce(self.player.rect.centerx)
                game_state = self.player.take_damage(1, enemy.rect.centerx)
                
        
        # Отрисовка
        self.screen.fill(BACK_BLUE)
        self.all_sprites.add(*self.wave_system.enemies)
        self.all_sprites.draw(self.screen)
        
        self.wave_system.enemies.draw(self.screen)
        self.wave_system.stars.draw(self.screen)
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

    
