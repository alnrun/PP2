import pygame
import datetime
import math

class MickeyClock:
    def __init__(self, screen):
        self.screen = screen
        self.width = 800
        self.height = 600
        self.center = (400, 300)

        self.clock_bg = pygame.image.load("images/clock.png").convert_alpha()
        self.clock_bg = pygame.transform.scale(self.clock_bg, (800, 600))

        self.mickey = pygame.image.load("images/mikkey.png").convert_alpha()
        self.mickey = pygame.transform.scale(self.mickey, (280, 340))

        self.hand_right = pygame.image.load("images/hand_right_centered.png").convert_alpha()
        self.hand_right = pygame.transform.scale(self.hand_right, (100, 200))

        self.hand_left = pygame.image.load("images/hand_left_centered.png").convert_alpha()
        self.hand_left = pygame.transform.scale(self.hand_left, (100, 200))

    def rotate_and_blit(self, image, angle, length):
        rotated = pygame.transform.rotate(image, -angle)
        rect = rotated.get_rect()

        rad = math.radians(angle - 90)
        offset_x = math.cos(rad) * length // 2
        offset_y = math.sin(rad) * length // 2

        rect.center = (
            self.center[0] + int(offset_x),
            self.center[1] + int(offset_y)
        )
        self.screen.blit(rotated, rect)

    def draw(self):
        now = datetime.datetime.now()
        minute_angle = now.minute * 6
        second_angle = now.second * 6

        # 1. Фон
        self.screen.blit(self.clock_bg, (0, 0))

        # 2. Правая рука = минуты
        self.rotate_and_blit(self.hand_right, minute_angle, 160)

        # 3. Левая рука = секунды
        self.rotate_and_blit(self.hand_left, second_angle, 160)

        # 4. Микки в центре
        mickey_rect = self.mickey.get_rect(center=self.center)
        self.screen.blit(self.mickey, mickey_rect)