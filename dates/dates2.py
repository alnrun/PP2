import pygame
import time

# Инициализация Pygame
pygame.init()

# Создание окна
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Моя первая игра")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
x, y = 320, 240

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= 5
    if keys[pygame.K_RIGHT]:
        x += 5
    if keys[pygame.K_UP]:
        y -= 5
    if keys[pygame.K_DOWN]:
        y += 5
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (x, y, 50, 50))
    pygame.time.delay(100)
    pygame.display.flip()
        
pygame.quit()