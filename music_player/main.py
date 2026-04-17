import pygame
import sys
from player import MusicPlayer

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Music Player")
clock = pygame.time.Clock()

player = MusicPlayer(music_folder="music")

font_large = pygame.font.SysFont("Arial", 32)
font_medium = pygame.font.SysFont("Arial", 22)
font_small = pygame.font.SysFont("Arial", 16)

# Цвета
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (0, 200, 100)
GRAY = (150, 150, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.prev_track()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    # Отрисовка UI
    screen.fill(BG_COLOR)

    # Заголовок
    title = font_large.render("🎵 Music Player", True, ACCENT_COLOR)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))

    # Текущий трек
    track_text = font_medium.render(f"Track: {player.get_track_name()}", True, TEXT_COLOR)
    screen.blit(track_text, (SCREEN_WIDTH // 2 - track_text.get_width() // 2, 130))

    # Статус
    status_text = font_medium.render(player.get_status(), True, ACCENT_COLOR)
    screen.blit(status_text, (SCREEN_WIDTH // 2 - status_text.get_width() // 2, 180))

    # Управление
    controls = [
        "[P] Play    [S] Stop",
        "[N] Next    [B] Back",
        "[Q] Quit"
    ]
    for i, line in enumerate(controls):
        ctrl = font_small.render(line, True, GRAY)
        screen.blit(ctrl, (SCREEN_WIDTH // 2 - ctrl.get_width() // 2, 270 + i * 28))

    pygame.display.flip()
    clock.tick(30)