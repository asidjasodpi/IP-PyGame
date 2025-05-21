import pygame
from settings import *
from score_manager import load_score, save_score

class Menu:
    def __init__(self, screen, high_score):
        self.screen = screen
        self.high_score = high_score  # Сохраняем рекорд
        self.font = pygame.font.SysFont("Arial", 40)
        self.small_font = pygame.font.SysFont("Arial", 24)
        
    def update(self):
        self.screen.fill(BLACK)
        
        # Отображаем рекорд
        # high_score_text = self.small_font.render(f"Рекорд: {self.high_score}", True, WHITE)
        # self.screen.blit(high_score_text, (20, 20))
        
        # Кнопки
        play_text = self.font.render("Играть", True, WHITE)
        score_text = self.font.render("Счёт", True, WHITE)
        exit_text = self.font.render("Выход", True, WHITE)
        
        self.screen.blit(play_text, (300, 200))
        self.screen.blit(score_text, (300, 300))
        self.screen.blit(exit_text, (300, 400))
        
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
        self.high_score =  load_score()
        # Показываем экран с рекордами
        self.screen.fill(BLACK)
        score_title = self.font.render("Лучший счёт:", True, WHITE)
        score_value = self.font.render(str(self.high_score), True, GREEN)
        
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
                    if event.key == pygame.K_r:
                        save_score(0)
                        waiting = False
                        

    def show_game_result(self, score, high_score, result):
        self.screen.fill(BLACK)

        title_font = pygame.font.SysFont("Arial", 48)
        font = pygame.font.SysFont("Arial", 32)

        if result == 'Ты победил':
            color = GREEN
        else:
            color = RED
        title = title_font.render(result, True, color)
        current_score = font.render(f"Ваш счёт: {score}", True, WHITE)
        best_score = font.render(f"Рекорд: {high_score}", True, GREEN)
        prompt = self.small_font.render("Нажмите любую клавишу, чтобы вернуться в меню", True, WHITE)

        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        self.screen.blit(current_score, (SCREEN_WIDTH // 2 - current_score.get_width() // 2, 230))
        self.screen.blit(best_score, (SCREEN_WIDTH // 2 - best_score.get_width() // 2, 280))
        self.screen.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 350))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key != pygame.K_LEFT and event.key != pygame.K_RIGHT:
                        waiting = False

    # def show_win_screen(self):
    #     self.screen.fill(BLACK)
    #     text = self.font.render("Ты победил!", True, GREEN)
    #     self.screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
    #     pygame.display.flip()
    #     pygame.time.delay(2000)