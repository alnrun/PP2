# Snake Game
# New features: weighted food types, food disappears after a timer

import pygame, sys, random
from pygame.locals import *

pygame.init()

CELL   = 20
COLS   = 30
ROWS   = 25
WIDTH  = COLS * CELL
HEIGHT = ROWS * CELL + 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# Colors
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GREEN      = (0,   200, 0)
DARK_GREEN = (0,   130, 0)
RED        = (220, 50,  50)
ORANGE     = (255, 140, 0)
CYAN       = (0,   210, 210)
BLUE       = (50,  80,  180)
GOLD       = (255, 215, 0)
BG         = (30,  30,  30)

font = pygame.font.SysFont("Consolas", 22, bold=True)

# Food types: (color, points, lifetime_seconds, weight)
# lifetime None = food never disappears
FOOD_TYPES = [
    (RED,    10, None, 60),  # normal  - common,   never expires
    (ORANGE, 25,  7,   30),  # rare    - uncommon, disappears in 7s
    (CYAN,   50,  4,   10),  # super   - rare,     disappears in 4s
]


def cell_rect(col, row):
    return pygame.Rect(col * CELL, row * CELL + 40, CELL, CELL)


def new_food(snake):
    # Pick a food type by weight
    weights = [f[3] for f in FOOD_TYPES]
    food_color, food_points, food_lifetime, _ = random.choices(FOOD_TYPES, weights=weights)[0]

    # Find a free cell not occupied by the snake
    while True:
        col = random.randint(1, COLS - 2)
        row = random.randint(1, ROWS - 2)
        if (col, row) not in snake:
            spawn_time = pygame.time.get_ticks()  # record when food appeared
            return (col, row), food_color, food_points, food_lifetime, spawn_time


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
    snake = [(COLS // 2, ROWS // 2),
             (COLS // 2 - 1, ROWS // 2),
             (COLS // 2 - 2, ROWS // 2)]
    direction = (1, 0)
    food_pos, food_color, food_points, food_lifetime, spawn_time = new_food(snake)
    return snake, direction, food_pos, food_color, food_points, food_lifetime, spawn_time, 0, 1, 0, 8


snake, direction, food_pos, food_color, food_points, food_lifetime, spawn_time, score, level, eaten, fps = reset()

# Main game loop
while True:
    now = pygame.time.get_ticks()  # current time in milliseconds

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); sys.exit()
        if event.type == KEYDOWN:
            if event.key in (K_UP,    K_w) and direction != (0,  1): direction = (0, -1)
            if event.key in (K_DOWN,  K_s) and direction != (0, -1): direction = (0,  1)
            if event.key in (K_LEFT,  K_a) and direction != (1,  0): direction = (-1, 0)
            if event.key in (K_RIGHT, K_d) and direction != (-1, 0): direction = (1,  0)

    # Check if food timer expired -> spawn new food
    if food_lifetime is not None:
        elapsed = (now - spawn_time) / 1000  # ms to seconds
        if elapsed >= food_lifetime:
            food_pos, food_color, food_points, food_lifetime, spawn_time = new_food(snake)

    # Move head one step in current direction
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

    # Wall collision
    if new_head[0] <= 0 or new_head[0] >= COLS - 1 or new_head[1] <= 0 or new_head[1] >= ROWS - 1:
        screen.fill(BLACK)
        screen.blit(font.render("GAME OVER", True, RED),       (WIDTH // 2 - 80, HEIGHT // 2 - 20))
        screen.blit(font.render("Press any key", True, WHITE), (WIDTH // 2 - 80, HEIGHT // 2 + 20))
        pygame.display.flip()
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == QUIT: pygame.quit(); sys.exit()
                if e.type == KEYDOWN: waiting = False
        snake, direction, food_pos, food_color, food_points, food_lifetime, spawn_time, score, level, eaten, fps = reset()
        continue

    # Self collision
    if new_head in snake:
        screen.fill(BLACK)
        screen.blit(font.render("GAME OVER", True, RED),       (WIDTH // 2 - 80, HEIGHT // 2 - 20))
        screen.blit(font.render("Press any key", True, WHITE), (WIDTH // 2 - 80, HEIGHT // 2 + 20))
        pygame.display.flip()
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == QUIT: pygame.quit(); sys.exit()
                if e.type == KEYDOWN: waiting = False
        snake, direction, food_pos, food_color, food_points, food_lifetime, spawn_time, score, level, eaten, fps = reset()
        continue

    snake.insert(0, new_head)  # add new head

    if new_head == food_pos:
        score += food_points   # award points based on food type
        eaten += 1
        food_pos, food_color, food_points, food_lifetime, spawn_time = new_food(snake)
        if eaten >= 4:          # level up every 4 foods eaten
            level += 1
            eaten  = 0
            fps    = 8 + (level - 1) * 2
            screen.fill(BLACK)
            screen.blit(font.render(f"LEVEL {level}!", True, GOLD), (WIDTH // 2 - 60, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(700)
    else:
        snake.pop()  # remove tail only when no food eaten

    # Draw everything
    screen.fill(BG)
    draw_walls()

    for i, (c, r) in enumerate(snake):
        pygame.draw.rect(screen, DARK_GREEN if i == 0 else GREEN, cell_rect(c, r))
        pygame.draw.rect(screen, BLACK, cell_rect(c, r), 1)

    # Blink food when less than 2 seconds remain on its timer
    show_food = True
    if food_lifetime is not None:
        remaining = food_lifetime - (now - spawn_time) / 1000
        if remaining < 2 and int(remaining / 0.3) % 2 == 0:
            show_food = False

    if show_food:
        pygame.draw.ellipse(screen, food_color, cell_rect(food_pos[0], food_pos[1]))

    draw_hud(score, level)
    pygame.display.flip()
    clock.tick(fps)