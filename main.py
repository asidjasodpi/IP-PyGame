import pygame
from settings import *
from menu import Menu
from level import Level

from score_manager import load_score, save_score

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("music/menu.mp3")
    pygame.mixer.music.play(-1)  # -1 = бесконечно
    pygame.mixer.music.set_volume(0.5)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
            
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.fadeout(2000)
                pygame.mixer.music.load("music/menu.mp3")
                pygame.mixer.music.play(-1)  # -1 = бесконечно
            game_state = menu.update()
            if game_state == "game":
                
                pygame.mixer.music.stop()
                if pygame.mixer.music.get_pos() == -1:  # Если музыка не играет
                    pygame.mixer.music.fadeout(300)
                    pygame.mixer.music.load("music/level_music.mp3")
                    pygame.mixer.music.play(-1)  # -1 = бесконечно
                level = Level(screen)
        elif game_state == "game":
            game_state = level.update()
            
        elif game_state == "game_over":
            pygame.mixer.music.stop()
            # Проверяем, побил ли игрок рекорд
            if level.player.score > high_score:
                high_score = level.player.score
                save_score(high_score)
            menu.show_game_result(level.player.score, high_score, "Ты проиграл")
            game_state = menu.update()  # Возвращаемся в меню

        elif game_state == "win":
            pygame.mixer.music.stop()
            if level.player.score > high_score:
                high_score = level.player.score
                save_score(high_score)
            menu.show_game_result(level.player.score, high_score, "Ты победил")
            game_state = menu.update()
            
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()