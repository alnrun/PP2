import pygame
pygame.init()
screen = pygame.display.set_mode((600,300))
pygame.display.set_caption("alnrun")


square = pygame.Surface((50,170))
square.fill('blue')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
        
pygame.quit()
