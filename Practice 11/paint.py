import pygame, sys, math
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 800, 580
TOOLBAR = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint  |  P=Pencil  R=Rect  Q=Square  C=Circle  E=Eraser  T=RTri  G=ETri  H=Rhombus  DEL=Clear")
clock  = pygame.time.Clock()

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR))
canvas.fill((255, 255, 255))

PALETTE = [
    (0,   0,   0),
    (255, 255, 255),
    (220, 50,  50),
    (50,  180, 50),
    (50,  100, 220),
    (255, 215, 0),
    (255, 140, 0),
    (160, 50,  200),
    (0,   200, 220),
    (255, 105, 180),
    (139, 90,  43),
    (150, 150, 150),
]

font = pygame.font.SysFont("Arial", 13, bold=True)

tool       = "pencil"
color      = (0, 0, 0)
size       = 6
start_pos  = None
CANVAS_TOP = HEIGHT - TOOLBAR

# All tools shown in toolbar
TOOLS = ["pencil", "rect", "square", "circle", "eraser", "rtri", "etri", "rhombus"]


# --- New shape drawing functions ---

def draw_square(surface, col, x1, y1, x2, y2):
    # Force equal width and height (use smaller side)
    side = min(abs(x2 - x1), abs(y2 - y1))
    sx = x1 + (side if x2 > x1 else -side)
    sy = y1 + (side if y2 > y1 else -side)
    x, y = min(x1, sx), min(y1, sy)
    pygame.draw.rect(surface, col, (x, y, side, side), 2)

def draw_right_triangle(surface, col, x1, y1, x2, y2):
    # Right angle sits at bottom-left corner
    pts = [(x1, y2), (x1, y1), (x2, y2)]
    pygame.draw.polygon(surface, col, pts, 2)

def draw_equilateral_triangle(surface, col, x1, y1, x2, y2):
    # Base goes from (x1,y2) to (x2,y2), apex is centred above
    base  = abs(x2 - x1)
    h     = int(base * math.sqrt(3) / 2)
    top_x = (x1 + x2) // 2
    top_y = max(y1, y2) - h
    pts   = [(x1, max(y1, y2)), (x2, max(y1, y2)), (top_x, top_y)]
    pygame.draw.polygon(surface, col, pts, 2)

def draw_rhombus(surface, col, x1, y1, x2, y2):
    # Vertices are the 4 midpoints of the bounding box
    mx, my = (x1 + x2) // 2, (y1 + y2) // 2
    pts = [(mx, y1), (x2, my), (mx, y2), (x1, my)]
    pygame.draw.polygon(surface, col, pts, 2)


def draw_toolbar():
    pygame.draw.rect(screen, (210, 210, 210), (0, CANVAS_TOP, WIDTH, TOOLBAR))
    pygame.draw.line(screen, (80, 80, 80), (0, CANVAS_TOP), (WIDTH, CANVAS_TOP), 2)

    # Tool buttons - two rows of 4
    for i, t in enumerate(TOOLS):
        bx = 2 + (i % 4) * 72
        by = CANVAS_TOP + 2 + (i // 4) * 27
        bg = (60, 60, 60) if t == tool else (160, 160, 160)
        pygame.draw.rect(screen, bg, (bx, by, 68, 23), border_radius=4)
        lbl = font.render(t, True, (255, 255, 255) if t == tool else (0, 0, 0))
        screen.blit(lbl, (bx + 34 - lbl.get_width() // 2, by + 5))

    # Color swatches
    for i, c in enumerate(PALETTE):
        sx = 295 + i * 34
        sy = CANVAS_TOP + 10
        pygame.draw.rect(screen, c, (sx, sy, 30, 30), border_radius=4)
        border = (220, 0, 0) if c == color else (80, 80, 80)
        pygame.draw.rect(screen, border, (sx, sy, 30, 30), 3, border_radius=4)

    # Active color preview box
    pygame.draw.rect(screen, color, (WIDTH - 45, CANVAS_TOP + 10, 38, 38), border_radius=4)
    pygame.draw.rect(screen, (0, 0, 0), (WIDTH - 45, CANVAS_TOP + 10, 38, 38), 2, border_radius=4)


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
            if event.key == K_q: tool = "square"
            if event.key == K_c: tool = "circle"
            if event.key == K_e: tool = "eraser"
            if event.key == K_t: tool = "rtri"
            if event.key == K_g: tool = "etri"
            if event.key == K_h: tool = "rhombus"
            if event.key == K_DELETE: canvas.fill((255, 255, 255))
            if event.key in (K_EQUALS, K_PLUS): size = min(50, size + 2)
            if event.key == K_MINUS:            size = max(1,  size - 2)

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if my >= CANVAS_TOP:
                # Check tool button clicks
                for i, t in enumerate(TOOLS):
                    bx = 2 + (i % 4) * 72
                    by = CANVAS_TOP + 2 + (i // 4) * 27
                    if bx < mx < bx + 68 and by < my < by + 23:
                        tool = t
                # Check color swatch clicks
                for i, c in enumerate(PALETTE):
                    sx, sy = 295 + i * 34, CANVAS_TOP + 10
                    if sx < mx < sx + 30 and sy < my < sy + 30:
                        color = c
                        if tool == "eraser": tool = "pencil"
            else:
                start_pos = (mx, my)  # start drag for shapes

        if event.type == MOUSEBUTTONUP and event.button == 1:
            if start_pos and my < CANVAS_TOP:
                x1, y1 = start_pos
                x2, y2 = mx, my
                x, y = min(x1, x2), min(y1, y2)
                w, h  = abs(x2 - x1), abs(y2 - y1)

                if tool == "rect":
                    pygame.draw.rect(canvas, color, (x, y, w, h), 2)
                elif tool == "square":
                    draw_square(canvas, color, x1, y1, x2, y2)
                elif tool == "circle" and w > 0 and h > 0:
                    pygame.draw.ellipse(canvas, color, (x, y, w, h), 2)
                elif tool == "rtri":
                    draw_right_triangle(canvas, color, x1, y1, x2, y2)
                elif tool == "etri":
                    draw_equilateral_triangle(canvas, color, x1, y1, x2, y2)
                elif tool == "rhombus":
                    draw_rhombus(canvas, color, x1, y1, x2, y2)
            start_pos = None

        if event.type == MOUSEWHEEL:
            size = max(1, min(50, size + event.y))

    # Freehand pencil / eraser while holding mouse button
    if pygame.mouse.get_pressed()[0] and my < CANVAS_TOP:
        if tool == "pencil":
            pygame.draw.circle(canvas, color, (mx, my), size)
        if tool == "eraser":
            pygame.draw.circle(canvas, (255, 255, 255), (mx, my), size * 2)

    screen.blit(canvas, (0, 0))

    # Live preview while dragging a shape
    if start_pos and my < CANVAS_TOP:
        x1, y1 = start_pos
        x2, y2 = mx, my
        x, y = min(x1, x2), min(y1, y2)
        w, h  = abs(x2 - x1), abs(y2 - y1)

        if tool == "rect":
            pygame.draw.rect(screen, color, (x, y, w, h), 2)
        elif tool == "square":
            draw_square(screen, color, x1, y1, x2, y2)
        elif tool == "circle" and w > 0 and h > 0:
            pygame.draw.ellipse(screen, color, (x, y, w, h), 2)
        elif tool == "rtri":
            draw_right_triangle(screen, color, x1, y1, x2, y2)
        elif tool == "etri":
            draw_equilateral_triangle(screen, color, x1, y1, x2, y2)
        elif tool == "rhombus":
            draw_rhombus(screen, color, x1, y1, x2, y2)

    if my < CANVAS_TOP:
        pygame.draw.circle(screen, (80, 80, 80), (mx, my), size if tool != "eraser" else size * 2, 1)

    draw_toolbar()
    pygame.display.flip()
    clock.tick(60)