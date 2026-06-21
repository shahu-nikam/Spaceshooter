# draw_utils.py
# small reusable drawing helpers so we don't repeat the same blit/rect code everywhere

import pygame
from constants import W, WHITE, pwidth, pheight

def text(screen, t, x, y, c=WHITE, f=None):
    screen.blit(f.render(t, True, c), (x, y))


def center_text(screen, msg, y, color=WHITE, f=None):
    txt = f.render(msg, True, color)
    screen.blit(txt, (W // 2 - txt.get_width() // 2, y))


def draw_player(screen, player_img, x, y):
    # draws the ship and gives back its rect so gameplay.py can check collisions
    screen.blit(player_img, (x, y))
    return pygame.Rect(x, y, pwidth, pheight)


def draw_button(screen, rect, label, font, btn_click=None, btn_timer=0):
    # generic button with a hover highlight and a press-down effect
    from constants import BLUE, WHITE, YELLOW
    mouse_pos = pygame.mouse.get_pos()
    hovered   = rect.collidepoint(mouse_pos)
    offset    = 4 if btn_click == rect and btn_timer > 0 else 0
    color     = YELLOW if btn_click == rect and btn_timer > 0 else BLUE
    if hovered:
        color = (100, 255, 255)
    rr = pygame.Rect(rect.x, rect.y + offset, rect.w, rect.h - offset)
    pygame.draw.rect(screen, color, rr, border_radius=8)
    pygame.draw.rect(screen, WHITE, rr, 2, border_radius=8)
    text(screen, label, rr.x + 30, rr.y + 12, f=font)


def draw_stars(screen, stars, H, W):
    # moves each star down a bit and wraps it back to the top once it's off screen
    for s in stars:
        pygame.draw.circle(screen, (255, 255, 255), (s[0], s[1]), 2)
        s[1] += 1
        if s[1] > H:
            import random
            s[0] = random.randint(0, W)
            s[1] = 0
