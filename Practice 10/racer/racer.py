import pygame, sys, random, time
from pygame.locals import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE   = (0, 0, 255)
RED    = (255, 0, 0)
GREEN  = (0, 255, 0)
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
YELLOW = (255, 215, 0)
GRAY   = (100, 100, 100)

SCREEN_WIDTH  = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0

font       = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over  = font.render("Game Over", True, BLACK)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption("Racer")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((42, 70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE, SPEED
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            if SCORE % 5 == 0 and SPEED < 15:
                SPEED += 1  # speed up every 5 dodged enemies
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((42, 70))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)

    def move(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT]  and self.rect.left   > 0:             self.rect.move_ip(-5, 0)
        if pressed[K_RIGHT] and self.rect.right  < SCREEN_WIDTH:  self.rect.move_ip( 5, 0)
        if pressed[K_UP]    and self.rect.top    > 0:             self.rect.move_ip(0, -5)
        if pressed[K_DOWN]  and self.rect.bottom < SCREEN_HEIGHT: self.rect.move_ip(0,  5)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (10, 10), 10)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()  # remove coin if player missed it

P1          = Player()
E1          = Enemy()
enemies     = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

enemies.add(E1)
all_sprites.add(P1, E1)

SPAWN_COIN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_COIN, 3000)

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); sys.exit()
        if event.type == SPAWN_COIN:
            c = Coin()
            coins_group.add(c)
            all_sprites.add(c)

    # Draw road
    screen.fill(GRAY)
    pygame.draw.rect(screen, GREEN, (0, 0, 50, SCREEN_HEIGHT))           # left grass
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH - 50, 0, 50, SCREEN_HEIGHT))  # right grass

    # Score – top left
    screen.blit(font_small.render("Score: " + str(SCORE), True, WHITE), (10, 10))

    # Coin counter – top right (extra feature)
    coin_text = font_small.render("Coins: " + str(COINS), True, YELLOW)
    screen.blit(coin_text, (SCREEN_WIDTH - coin_text.get_width() - 10, 10))

    # Move and draw every sprite
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    # Collect coins
    COINS += len(pygame.sprite.spritecollide(P1, coins_group, True))

    # Enemy collision → Game Over
    if pygame.sprite.spritecollideany(P1, enemies):
        screen.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit(); sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)