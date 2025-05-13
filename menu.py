import pygame
from settings import *
class Menu:
    def __init__(self, screen, high_score):
        self.screen = screen
        self.high_score = high_score
        self.small_font = pygame.font.SysFont("Arial", 24)
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
        self.screen.fill(BLACK)
        score_title = self.font.render("Лучший счёт", True, WHITE)
        score_value = self.font.render(str(self.high_score), True, G)

        self.screen.blit(score_title, (300, 200))
        self.screen.blit(score_value, (350, 300))

        back_text = self.small_font.render("Назад (ESC)", True, WHITE)
        self.screen.blit(back_text, (20, 20))

        pygame.display.flip()
        clock = pygame.time.Clock()
        waiting = True
        while waiting:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
    def show_game_result(self, score, high_score):
        self.screen.fill(BLACK)

        title_font = pygame.font.SysFont("Arial", 48)
        font = pygame.font.SysFont("Arial", 32)

        title = title_font.render("Игра окончена!", True, R)
        current_score = font.render(f"Ваш счёт: {score}", True, WHITE)
        best_score = font.render(f"Рекорд: {high_score}", True, G)
        prompt = self.small_font.render("Нажмите на любую клавишу, чтобы вернуться в меню", True, WHITE)

        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))
        self.screen.blit(current_score, (WIDTH // 2 - current_score.get_width() // 2, 230))
        self.screen.blit(best_score, (WIDTH // 2 - best_score.get_width() // 2, 280))
        self.screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 350))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting = False