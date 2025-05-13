import pygame
from settings import *
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 40)

    def update(self):
        self.screen.fill(BLACK)

        #Кнопки
        play_text = self.font.render("Играть", True, WHITE)
        score_text = self.font.render("Счёт", True, WHITE)
        exit_text = self.font.render("Выйти", True, WHITE)

        self.screen.blit(play_text, (300,200))
        self.screen.blit(score_text, (300,300))
        self.screen.blit(exit_text, (300,400))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 300 <= mouse[0] <= 500 and 200 <= mouse[1] <= 250:
            if click[0]:
                return "game"
        
        if 300 <= mouse[0] <= 500 and 300 <= mouse[1] <= 350:
            if click[0]:
                self.show_score()

        if 300 <= mouse[0] <= 500 and 400 <= mouse[1] <= 450:
            if click[0]:
                pygame.quit()
                exit()

        return "menu"
    
    def show_score(self):
        pass