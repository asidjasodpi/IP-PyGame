import pygame
from settings import *
from player import Player
from enemy import Enemy, WaveSystem

class Level: 
    def __init__(self, screen):
        self.screen = screen
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.player = None
        self.wave_system = None
        self.setup_level()

    def setup_level(self):
        # Создаём игрока
        self.player = Player (100, HEIGHT - 100)
        self.all_sprites.add(self.player)
        # Создаём платформы (простые прямоугольники)
        ground = pygame.sprite.Sprite()
        ground.image = pygame. Surface ((WIDTH, 20))
        ground.image.fill(WHITE)
        ground.rect = ground.image.get_rect()
        ground.rect.x = 0
        ground.rect.y = HEIGHT - 20
        self.platforms.add(ground)
        self.all_sprites.add(ground)

        # Добавляем ещё платформы (можно настроить как угодно)
        platform1 = pygame.sprite.Sprite()
        platform1.image = pygame. Surface ((200, 20))
        platform1.image.fill(WHITE)
        platform1.rect = platform1.image.get_rect()
        platform1.rect.x = 300
        platform1.rect.y = 400
        self.platforms.add(platform1)
        self.all_sprites.add(platform1)

        platform2 = pygame.sprite.Sprite()
        platform2.image = pygame. Surface ((200, 20))
        platform2.image.fill(WHITE)
        platform2.rect = platform2.image.get_rect()
        platform2.rect.x = 100
        platform2.rect.y = 300
        self.platforms.add(platform2)
        self.all_sprites.add(platform2)

        #Инициализируем систему волн
        self.wave_system = WaveSystem()

    def update(self):
        #Обновляем все спрайты
        self.all_sprites.update()

        #Проверяем столкновения игрока с платформами
        if self.player.is_jumping:
        # Гравитация (падение)
            self.player.rect.y += 5

            # Проверяем, приземлился ли игрок
            platform_collisions = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if platform_collisions:
                self.player.is_jumping = False
                self.player.rect.bottom = platform_collisions[0].rect.top

        #Обновляем волны врагов
        game_state = self.wave_system.update() 
        if game_state != "game": 
            return game_state # "win" или "game_over"
        
        # # Проверяем столкновения пуль с врагами
        # for enemy in self.wave_system.enemies:
        # if pygame.sprite.spritecollide (enemy, self.player.bullets, True):
        # enemy.kill()
        # self.player.add_score(10)

        # Проверяем столкновения игрока с врагами
        if pygame.sprite.spritecollide(self.player, self.wave_system.enemies, False):
            game_state = self.player.take_damage (10)
            if game_state == "game_over":
                return game_state
            
        # Отрисовываем всё
        self.screen.fill (BLACK)
        self.all_sprites.draw(self.screen)
        self.wave_system.enemies.draw(self.screen)
        # self.player.bullets.draw(self.screen)
        # Отображаем здоровье и счёт
        self.draw_hud()
        return "game"
    def draw_hud(self):
        # Здоровье
        health_text = pygame.font. SysFont("Arial", 24).render(
            f"Здоровье: {self.player.health}", True, WHITE
        )
        self.screen.blit (health_text, (20, 20))
        # Счёт
        score_text = pygame.font. SysFont("Arial", 24).render (
             f"Счёт: {self.player.score}", True, WHITE
        )
        self.screen.blit(score_text, (20, 50))
        # Волна
        wave_text = pygame.font.SysFont("Arial", 24).render( 
            f"Волна: {self.wave_system.wave}/{self.wave_system.max_waves}", True, WHITE 
        ) 
        self.screen.blit(wave_text, (20, 80))