# Snake Game – extended from lecture base
# Features: wall collision, smart food spawn, levels, speed increase, score/level display

import pygame, sys, random
from pygame.locals import *

pygame.init()

CELL   = 20
COLS   = 30
ROWS   = 25
WIDTH  = COLS * CELL        # 600
HEIGHT = ROWS * CELL + 40   # 500 + 40px score bar

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# Colors
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GREEN      = (0,   200, 0)
DARK_GREEN = (0,   130, 0)
RED        = (220, 50,  50)
BLUE       = (50,  80,  180)
GOLD       = (255, 215, 0)
BG         = (30,  30,  30)

font = pygame.font.SysFont("Consolas", 22, bold=True)


def cell_rect(col, row):
    # Convert grid position to pixel rectangle (+40 for score bar offset)
    return pygame.Rect(col * CELL, row * CELL + 40, CELL, CELL)


def new_food(snake):
    # Keep picking random cells until one is not on a wall or the snake
    while True:
        col = random.randint(1, COLS - 2)
        row = random.randint(1, ROWS - 2)
        if (col, row) not in snake:
            return (col, row)


def draw_walls():
    for c in range(COLS):
        for r in range(ROWS):
            if c == 0 or c == COLS - 1 or r == 0 or r == ROWS - 1:
                pygame.draw.rect(screen, BLUE, cell_rect(c, r))


def draw_hud(score, level):
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 40))
    screen.blit(font.render(f"Score: {score}", True, GOLD),  (10, 8))
    screen.blit(font.render(f"Level: {level}", True, WHITE), (WIDTH // 2 - 50, 8))


def reset():
    snake     = [(COLS // 2, ROWS // 2),
                 (COLS // 2 - 1, ROWS // 2),
                 (COLS // 2 - 2, ROWS // 2)]
    direction = (1, 0)   # start moving right
    food      = new_food(snake)
    return snake, direction, food, 0, 1, 0, 8  # snake, dir, food, score, level, eaten, fps


snake, direction, food, score, level, eaten, fps = reset()

# Main game loop
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); sys.exit()
        if event.type == KEYDOWN:
            if event.key in (K_UP,    K_w) and direction != (0,  1): direction = (0, -1)
            if event.key in (K_DOWN,  K_s) and direction != (0, -1): direction = (0,  1)
            if event.key in (K_LEFT,  K_a) and direction != (1,  0): direction = (-1, 0)
            if event.key in (K_RIGHT, K_d) and direction != (-1, 0): direction = (1,  0)

    # Calculate new head position
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    # 1. Wall collision check
    if new_head[0] <= 0 or new_head[0] >= COLS - 1 or new_head[1] <= 0 or new_head[1] >= ROWS - 1:
        screen.fill(BLACK)
        screen.blit(font.render("GAME OVER", True, RED),   (WIDTH // 2 - 80, HEIGHT // 2 - 20))
        screen.blit(font.render("Press any key", True, WHITE), (WIDTH // 2 - 80, HEIGHT // 2 + 20))
        pygame.display.flip()
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == QUIT: pygame.quit(); sys.exit()
                if e.type == KEYDOWN: waiting = False
        snake, direction, food, score, level, eaten, fps = reset()
        continue

    # Self collision check
    if new_head in snake:
        screen.fill(BLACK)
        screen.blit(font.render("GAME OVER", True, RED),   (WIDTH // 2 - 80, HEIGHT // 2 - 20))
        screen.blit(font.render("Press any key", True, WHITE), (WIDTH // 2 - 80, HEIGHT // 2 + 20))
        pygame.display.flip()
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == QUIT: pygame.quit(); sys.exit()
                if e.type == KEYDOWN: waiting = False
        snake, direction, food, score, level, eaten, fps = reset()
        continue

    snake.insert(0, new_head)  # add new head

    if new_head == food:
        score += 10
        eaten += 1
        food = new_food(snake)  # 2. spawn food not on wall or snake
        if eaten >= 4:           # 3. level up every 4 foods
            level += 1
            eaten  = 0
            fps    = 8 + (level - 1) * 2  # 4. increase speed each level
            screen.fill(BLACK)
            screen.blit(font.render(f"LEVEL {level}!", True, GOLD), (WIDTH // 2 - 60, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(700)
    else:
        snake.pop()  # remove tail only when no food eaten

    # Draw
    screen.fill(BG)
    draw_walls()

    for i, (c, r) in enumerate(snake):
        pygame.draw.rect(screen, DARK_GREEN if i == 0 else GREEN, cell_rect(c, r))
        pygame.draw.rect(screen, BLACK, cell_rect(c, r), 1)

    pygame.draw.ellipse(screen, RED, cell_rect(food[0], food[1]))

    draw_hud(score, level)  # 5. score and level counter

    pygame.display.flip()
    clock.tick(fps)