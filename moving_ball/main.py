import pygame
import sys
from ball import Ball

# Инициализация
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Ball Game")
clock = pygame.time.Clock()

ball = Ball(SCREEN_WIDTH, SCREEN_HEIGHT)

# Главный цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ball.move(0, -ball.speed)
            elif event.key == pygame.K_DOWN:
                ball.move(0, ball.speed)
            elif event.key == pygame.K_LEFT:
                ball.move(-ball.speed, 0)
            elif event.key == pygame.K_RIGHT:
                ball.move(ball.speed, 0)
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    # Отрисовка
    screen.fill((255, 255, 255))  # Белый фон
    ball.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)