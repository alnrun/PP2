import pygame, sys
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 800, 580
TOOLBAR = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint  |  P=Pencil  R=Rect  C=Circle  E=Eraser  DEL=Clear")
clock  = pygame.time.Clock()

# Canvas is the white drawing area above the toolbar
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR))
canvas.fill((255, 255, 255))

# Color palette
PALETTE = [
    (0,   0,   0),    # black
    (255, 255, 255),  # white
    (220, 50,  50),   # red
    (50,  180, 50),   # green
    (50,  100, 220),  # blue
    (255, 215, 0),    # yellow
    (255, 140, 0),    # orange
    (160, 50,  200),  # purple
    (0,   200, 220),  # cyan
    (255, 105, 180),  # pink
    (139, 90,  43),   # brown
    (150, 150, 150),  # gray
]

font = pygame.font.SysFont("Arial", 15, bold=True)

# Current state
tool       = "pencil"       # pencil / rect / circle / eraser
color      = (0, 0, 0)
size       = 6              # brush radius
start_pos  = None           # for shape drag-and-drop
CANVAS_TOP = HEIGHT - TOOLBAR


def draw_toolbar():
    pygame.draw.rect(screen, (210, 210, 210), (0, CANVAS_TOP, WIDTH, TOOLBAR))
    pygame.draw.line(screen, (80, 80, 80), (0, CANVAS_TOP), (WIDTH, CANVAS_TOP), 2)

    # Tool buttons
    for i, t in enumerate(["pencil", "rect", "circle", "eraser"]):
        bx = 10 + i * 80
        by = CANVAS_TOP + 10
        bg = (60, 60, 60) if t == tool else (160, 160, 160)
        pygame.draw.rect(screen, bg, (bx, by, 70, 38), border_radius=6)
        lbl = font.render(t, True, (255, 255, 255) if t == tool else (0, 0, 0))
        screen.blit(lbl, (bx + 35 - lbl.get_width() // 2, by + 12))

    # Color swatches
    for i, c in enumerate(PALETTE):
        sx = 340 + i * 36
        sy = CANVAS_TOP + 12
        pygame.draw.rect(screen, c, (sx, sy, 32, 32), border_radius=4)
        border = (220, 0, 0) if c == color else (80, 80, 80)
        pygame.draw.rect(screen, border, (sx, sy, 32, 32), 3, border_radius=4)

    # Selected color preview
    pygame.draw.rect(screen, color, (WIDTH - 50, CANVAS_TOP + 10, 38, 38), border_radius=4)
    pygame.draw.rect(screen, (0, 0, 0), (WIDTH - 50, CANVAS_TOP + 10, 38, 38), 2, border_radius=4)


# Main loop
while True:
    mx, my = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); sys.exit()

        # Keyboard shortcuts
        if event.type == KEYDOWN:
            if event.key == K_p: tool = "pencil"
            if event.key == K_r: tool = "rect"
            if event.key == K_c: tool = "circle"
            if event.key == K_e: tool = "eraser"
            if event.key == K_DELETE: canvas.fill((255, 255, 255))
            if event.key in (K_EQUALS, K_PLUS):  size = min(50, size + 2)
            if event.key == K_MINUS:             size = max(1,  size - 2)

        # Mouse button down
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if my >= CANVAS_TOP:
                # Click on a tool button
                for i, t in enumerate(["pencil", "rect", "circle", "eraser"]):
                    bx, by = 10 + i * 80, CANVAS_TOP + 10
                    if bx < mx < bx + 70 and by < my < by + 38:
                        tool = t
                # Click on a color swatch
                for i, c in enumerate(PALETTE):
                    sx, sy = 340 + i * 36, CANVAS_TOP + 12
                    if sx < mx < sx + 32 and sy < my < sy + 32:
                        color = c
                        if tool == "eraser": tool = "pencil"
            else:
                start_pos = (mx, my)  # start shape drag

        # Mouse button up – commit shape to canvas
        if event.type == MOUSEBUTTONUP and event.button == 1:
            if start_pos and my < CANVAS_TOP:
                x = min(start_pos[0], mx);  w = abs(mx - start_pos[0])
                y = min(start_pos[1], my);  h = abs(my - start_pos[1])
                if tool == "rect":
                    pygame.draw.rect(canvas, color, (x, y, w, h), 2)
                if tool == "circle" and w > 0 and h > 0:
                    pygame.draw.ellipse(canvas, color, (x, y, w, h), 2)
            start_pos = None

        if event.type == MOUSEWHEEL:
            size = max(1, min(50, size + event.y))

    # Freehand draw while mouse held
    if pygame.mouse.get_pressed()[0] and my < CANVAS_TOP:
        if tool == "pencil":
            pygame.draw.circle(canvas, color, (mx, my), size)
        if tool == "eraser":
            pygame.draw.circle(canvas, (255, 255, 255), (mx, my), size * 2)

    # Draw canvas, live shape preview, cursor, toolbar
    screen.blit(canvas, (0, 0))

    if start_pos and tool in ("rect", "circle") and my < CANVAS_TOP:
        x = min(start_pos[0], mx);  w = abs(mx - start_pos[0])
        y = min(start_pos[1], my);  h = abs(my - start_pos[1])
        if tool == "rect": pygame.draw.rect(screen, color, (x, y, w, h), 2)
        if tool == "circle" and w > 0 and h > 0: pygame.draw.ellipse(screen, color, (x, y, w, h), 2)

    if my < CANVAS_TOP:
        pygame.draw.circle(screen, (80, 80, 80), (mx, my), size if tool != "eraser" else size * 2, 1)

    draw_toolbar()
    pygame.display.flip()
    clock.tick(60)