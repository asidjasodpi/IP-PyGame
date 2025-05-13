import pygame
from settings import *
from menu import Menu
from level import Level

from score_manager import load_score, save_score

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Платформер")
    clock = pygame.time.Clock()
    
    high_score = load_score()  # Загружаем рекорд
    menu = Menu(screen, high_score)  # Передаём рекорд в меню
    level = Level(screen)
    
    game_state = "menu"
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # При выходе сохраняем счёт (если он больше рекорда)
                if level.player.score > high_score:
                    save_score(level.player.score)
                pygame.quit()
                return
            
        if game_state == "menu":
            game_state = menu.update()
            if game_state == "game":
                level = Level(screen)
        elif game_state == "game":
            game_state = level.update()
        elif game_state == "game_over":
            # Проверяем, побил ли игрок рекорд
            if level.player.score > high_score:
                high_score = level.player.score
                save_score(high_score)
            menu.show_game_result(level.player.score, high_score)
            game_state = menu.update()  # Возвращаемся в меню
        elif game_state == "win":
            if level.player.score > high_score:
                high_score = level.player.score
                save_score(high_score)
            menu.show_game_result(level.player.score, high_score)
            game_state = menu.update()
            
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()