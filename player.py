import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(G)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = PLAYER_SPEED
        self.jump_power = PLAYER_JUMP_POWER
        self.health = PLAYER_HEALTH
        self.score = 0
        self.is_jumping = False


    def update(self):
        keys = pygame.key.get_pressed()

        #Движение
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        # Прыжок
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.rect.y -= self.jump_power
        
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return "game_over"
        return "game"