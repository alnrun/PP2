import pygame
import sys
from clock import MickeyClock

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Mickey Mouse Clock")
    fps = pygame.time.Clock()

    clock = MickeyClock(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        clock.draw()
        pygame.display.flip()
        fps.tick(1)  # 1 раз в секунду

if __name__ == "__main__":
    main()