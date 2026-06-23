import pygame
import math
import random
from constants import W, H, RED, GREEN, BLUE, WHITE, YELLOW, MIN_SPEED, MAX_SPEED
from draw_utils import text, center_text

# button rects for the main menu
play = pygame.Rect(300, 190, 200, 46)
diff = pygame.Rect(300, 252, 200, 46)
setb = pygame.Rect(300, 314, 200, 46)
resb = pygame.Rect(300, 376, 200, 46)

# button rects for the difficulty screen
easy = pygame.Rect(90,  260, 140, 46)
med  = pygame.Rect(253, 260, 140, 46)
hard = pygame.Rect(416, 260, 140, 46)
ext  = pygame.Rect(579, 260, 140, 46)

DIFF_COLORS = {
    "Easy":    (40,  180, 40 ),
    "Medium":  (40,  130, 220),
    "Hard":    (220, 120, 0  ),
    "Extreme": (220, 40,  40 ),
}

_DIFF_DESCS = {
    "Easy":    "Chill — slow spawns",
    "Medium":  "Balanced — classic",
    "Hard":    "Fast — 2x points",
    "Extreme": "Chaos — 3x points",
}

# used to slow down how fast the speed slider changes when arrow keys are held
_spd_hold = {"L": 0, "R": 0}
_SPD_RPT  = 10


def _btn(screen, rect, label, font, color=BLUE, active=False, pressed=False):
    # draws one button - handles hover, active (selected) and pressed states
    mouse = pygame.mouse.get_pos()
    hover = rect.collidepoint(mouse)

    col = color
    if active:
        col = YELLOW
    elif pressed:
        col = tuple(max(0, c - 50) for c in col)
    elif hover:
        col = tuple(min(255, c + 45) for c in col)

    dr = rect.inflate(-4, -4) if pressed else rect

    pygame.draw.rect(screen, (0, 0, 0), dr.move(3, 3), border_radius=8)   # shadow
    pygame.draw.rect(screen, col, dr, border_radius=8)                    # body

    sh = pygame.Surface((dr.w - 8, dr.h // 3), pygame.SRCALPHA)           # top shine
    sh.fill((255, 255, 255, 30))
    screen.blit(sh, (dr.x + 4, dr.y + 3))

    pygame.draw.rect(screen, (200, 200, 200) if pressed else WHITE, dr, 1, border_radius=8)

    lbl = font.render(label, True, WHITE)
    screen.blit(lbl, (dr.x + (dr.w - lbl.get_width())//2,
                      dr.y + (dr.h - lbl.get_height())//2))


def draw_menu(screen, fonts, difficulty, player_img, menu_ship_x, btn_click, btn_timer):
    font = fonts["font"]; big = fonts["big"]; small = fonts["small"]

    # title text slowly shifts color using sine waves, looks nicer than a flat color
    t   = pygame.time.get_ticks()
    col = (int(190 + 65 * math.sin(t / 600)),
           int(190 + 65 * math.sin(t / 800 + 1)),
           255)
    title = big.render("SPACE  SHOOTER", True, col)
    screen.blit(title, (W//2 - title.get_width()//2, 70))

    pygame.draw.line(screen, (60, 60, 60), (200, 158), (600, 158), 1)

    for r, label in [(play,"PLAY"),(diff,"DIFFICULTY"),(setb,"SETTINGS"),(resb,"RESULTS")]:
        _btn(screen, r, label, font, pressed=(btn_click == r and btn_timer > 0))

    # shows currently picked difficulty as a little colored badge
    dc    = DIFF_COLORS.get(difficulty, WHITE)
    badge = pygame.Rect(W//2 - 75, 445, 150, 28)
    pygame.draw.rect(screen, dc, badge, border_radius=5)
    pygame.draw.rect(screen, WHITE, badge, 1, border_radius=5)
    bl = small.render(f"Mode : {difficulty}", True, WHITE)
    screen.blit(bl, (badge.x + (badge.w - bl.get_width())//2, badge.y + 5))

    hint = small.render("A / D  move     SPACE  shoot     ESC  menu", True, (80, 80, 80))
    screen.blit(hint, (W//2 - hint.get_width()//2, 500))

    screen.blit(player_img, (menu_ship_x, 540))


def draw_difficulty(screen, fonts, difficulty, btn_click, btn_timer):
    font = fonts["font"]; big = fonts["big"]; small = fonts["small"]

    title = big.render("DIFFICULTY", True, WHITE)
    screen.blit(title, (W//2 - title.get_width()//2, 130))
    pygame.draw.line(screen, (60, 60, 60), (150, 195), (650, 195), 1)

    for r, label in [(easy,"Easy"),(med,"Medium"),(hard,"Hard"),(ext,"Extreme")]:
        col     = DIFF_COLORS[label]
        active  = (difficulty == label)
        pressed = (btn_click == r and btn_timer > 0)
        _btn(screen, r, label, font, color=col, active=active, pressed=pressed)

        if active:
            ck = small.render("✓ selected", True, YELLOW)
            screen.blit(ck, (r.x + r.w//2 - ck.get_width()//2, r.y + 52))
        else:
            ds = small.render(_DIFF_DESCS[label], True, (140, 140, 140))
            screen.blit(ds, (r.x + r.w//2 - ds.get_width()//2, r.y + 52))

    # small preview card showing what the picked difficulty actually does
    dc   = DIFF_COLORS.get(difficulty, WHITE)
    info = {
        "Easy":    ("Spawn : 1.0s", "Speed : Slow", "Points : 1x"),
        "Medium":  ("Spawn : 0.67s","Speed : Normal","Points : 1x"),
        "Hard":    ("Spawn : 0.5s", "Speed : Fast", "Points : 2x"),
        "Extreme": ("Spawn : 0.33s","Speed : Max",  "Points : 3x"),
    }[difficulty]
    panel = pygame.Rect(W//2 - 130, 360, 260, 110)
    pygame.draw.rect(screen, (20, 20, 35), panel, border_radius=8)
    pygame.draw.rect(screen, dc, panel, 2, border_radius=8)
    ht = font.render(difficulty, True, dc)
    screen.blit(ht, (panel.x + (panel.w - ht.get_width())//2, panel.y + 10))
    for i, line in enumerate(info):
        ls = small.render(line, True, (200, 200, 200))
        screen.blit(ls, (panel.x + 20, panel.y + 44 + i * 22))

    text(screen, "ESC : Back", 20, 20, (100, 100, 100), fonts["small"])


def draw_results(screen, fonts, scores):
    font = fonts["font"]; big = fonts["big"]; small = fonts["small"]

    title = big.render("HIGH  SCORES", True, YELLOW)
    screen.blit(title, (W//2 - title.get_width()//2, 90))
    pygame.draw.line(screen, (60, 60, 60), (150, 158), (650, 158), 1)

    y = 200
    for k, v in scores.items():
        col   = DIFF_COLORS.get(k, WHITE)
        bar_w = min(280, v * 3)   # cap the bar so a huge score doesn't run off screen

        row = pygame.Rect(120, y - 4, 560, 38)
        pygame.draw.rect(screen, (18, 18, 28), row, border_radius=6)
        pygame.draw.rect(screen, (50, 50, 50), row, 1, border_radius=6)

        dl = font.render(k, True, col)
        screen.blit(dl, (140, y + 4))

        if bar_w > 0:
            pygame.draw.rect(screen, col, (270, y + 8, bar_w, 18), border_radius=4)

        sv = font.render(str(v), True, WHITE)
        screen.blit(sv, (560, y + 4))

        y += 52

    text(screen, "ESC : Back", 20, 20, (100, 100, 100), small)


def draw_settings(screen, fonts, pspeed, settings):
    font = fonts["font"]; big = fonts["big"]; small = fonts["small"]

    title = big.render("SETTINGS", True, WHITE)
    screen.blit(title, (W//2 - title.get_width()//2, 50))
    pygame.draw.line(screen, (60, 60, 60), (100, 112), (700, 112), 1)

    # player speed slider with < > buttons
    text(screen, "PLAYER SPEED", 100, 140, YELLOW, font)

    bx, by = W//2 - 10, 135
    lb = pygame.Rect(bx - 80, by, 32, 32)
    rb = pygame.Rect(bx + 50, by, 32, 32)
    mouse = pygame.mouse.get_pos()
    for btn, lbl in [(lb, "<"), (rb, ">")]:
        hov = btn.collidepoint(mouse)
        pygame.draw.rect(screen, (70, 70, 90) if not hov else (100, 100, 130), btn, border_radius=5)
        pygame.draw.rect(screen, WHITE, btn, 1, border_radius=5)
        al = font.render(lbl, True, WHITE)
        screen.blit(al, (btn.x + (btn.w - al.get_width())//2,
                         btn.y + (btn.h - al.get_height())//2))

    vbox = pygame.Rect(bx - 40, by, 82, 32)
    pygame.draw.rect(screen, (25, 25, 45), vbox, border_radius=5)
    pygame.draw.rect(screen, BLUE, vbox, 1, border_radius=5)
    vl = font.render(str(pspeed), True, WHITE)
    screen.blit(vl, (vbox.x + (vbox.w - vl.get_width())//2,
                     vbox.y + (vbox.h - vl.get_height())//2))

    bbar_x, bbar_y, bbar_w = 100, 180, 500
    pygame.draw.rect(screen, (45, 45, 45), (bbar_x, bbar_y, bbar_w, 10), border_radius=4)
    fill = int((pspeed - MIN_SPEED) / (MAX_SPEED - MIN_SPEED) * bbar_w)
    pygame.draw.rect(screen, BLUE, (bbar_x, bbar_y, fill, 10), border_radius=4)
    text(screen, str(MIN_SPEED), bbar_x - 18, bbar_y - 4, (100,100,100), small)
    text(screen, str(MAX_SPEED), bbar_x + bbar_w + 6, bbar_y - 4, (100,100,100), small)
    text(screen, "Arrow keys  or  click  <  >  to adjust", bbar_x, 198, (100,100,100), small)

    pygame.draw.line(screen, (50, 50, 50), (100, 228), (700, 228), 1)

    # sound toggle
    text(screen, "SOUND FX", 100, 252, YELLOW, font)
    snd_on = settings.get("sound", True)
    sr = pygame.Rect(100, 285, 100, 34)
    pygame.draw.rect(screen, GREEN if snd_on else (80,80,80), sr, border_radius=6)
    pygame.draw.rect(screen, WHITE, sr, 1, border_radius=6)
    sl = font.render("ON" if snd_on else "OFF", True, WHITE)
    screen.blit(sl, (sr.x + (sr.w - sl.get_width())//2, sr.y + (sr.h - sl.get_height())//2))
    text(screen, "Press  S  to toggle", 215, 292, (110,110,110), small)

    # music toggle
    text(screen, "MUSIC", 100, 345, YELLOW, font)
    mus_on = settings.get("music", True)
    mr = pygame.Rect(100, 378, 100, 34)
    pygame.draw.rect(screen, GREEN if mus_on else (80,80,80), mr, border_radius=6)
    pygame.draw.rect(screen, WHITE, mr, 1, border_radius=6)
    ml = font.render("ON" if mus_on else "OFF", True, WHITE)
    screen.blit(ml, (mr.x + (mr.w - ml.get_width())//2, mr.y + (mr.h - ml.get_height())//2))
    text(screen, "Press  M  to toggle", 215, 386, (110,110,110), small)

    # volume bar
    text(screen, "VOLUME", 100, 440, YELLOW, font)
    vol = settings.get("volume", 0.7)
    vb_x, vb_y, vb_w = 100, 475, 400
    pygame.draw.rect(screen, (45,45,45), (vb_x, vb_y, vb_w, 10), border_radius=4)
    pygame.draw.rect(screen, (80,180,255), (vb_x, vb_y, int(vol * vb_w), 10), border_radius=4)
    pygame.draw.rect(screen, (80,80,80), (vb_x, vb_y, vb_w, 10), 1, border_radius=4)
    text(screen, f"{int(vol*100)}%", vb_x + vb_w + 10, vb_y - 4, WHITE, font)
    text(screen, "-  /  +  keys to change volume", vb_x, 492, (110,110,110), small)

    text(screen, "ESC : Back", 20, 20, (100,100,100), small)

    # arrow key handling for speed slider - rate limited so it doesn't fly through values
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        _spd_hold["L"] += 1
        if _spd_hold["L"] == 1 or _spd_hold["L"] % _SPD_RPT == 0:
            if pspeed > MIN_SPEED: pspeed -= 1
    else:
        _spd_hold["L"] = 0
    if keys[pygame.K_RIGHT]:
        _spd_hold["R"] += 1
        if _spd_hold["R"] == 1 or _spd_hold["R"] % _SPD_RPT == 0:
            if pspeed < MAX_SPEED: pspeed += 1
    else:
        _spd_hold["R"] = 0

    return pspeed, settings


def draw_game_over(screen, fonts, game, scores, difficulty, over_timer):
    font  = fonts["font"]
    big   = fonts["big"]
    small = fonts["small"]
    t     = pygame.time.get_ticks()

    # quick red flash right after dying
    if over_timer < 25:
        alpha = int(180 * (1 - over_timer / 25))
        fl    = pygame.Surface((W, H), pygame.SRCALPHA)
        fl.fill((220, 0, 0, alpha))
        screen.blit(fl, (0, 0))

    # title slides down with a little shake for impact
    slide   = min(1.0, max(0.0, (over_timer - 8) / 25))
    title_y = int(-70 + slide * 90)
    shake   = random.randint(-3, 3) if over_timer < 40 else 0

    title = big.render("GAME  OVER", True, RED)
    screen.blit(title, (W//2 - title.get_width()//2 + shake, title_y + shake))

    if slide < 1.0:
        return   # wait for the slide-in to finish before showing the panel

    # result panel
    panel = pygame.Rect(W//2 - 220, 155, 440, 290)
    pygame.draw.rect(screen, (14, 14, 22), panel, border_radius=12)
    pygame.draw.rect(screen, (60, 60, 80), panel, 1, border_radius=12)

    py = panel.y + 18

    if game.get("new_record"):
        pulse = abs(math.sin(t / 220))
        rc    = (int(255*pulse), int(210*pulse), 0)
        nr    = font.render("★  NEW HIGH SCORE  ★", True, rc)
        screen.blit(nr, (W//2 - nr.get_width()//2, py))
        py += 38

    sc_s = font.render(f"Score     {game['score']}", True, WHITE)
    bs_s = font.render(f"Best      {scores[difficulty]}", True, (160, 210, 255))
    screen.blit(sc_s, (W//2 - sc_s.get_width()//2, py));       py += 36
    screen.blit(bs_s, (W//2 - bs_s.get_width()//2, py));       py += 30

    dc  = DIFF_COLORS.get(difficulty, WHITE)
    dtg = small.render(difficulty.upper(), True, dc)
    screen.blit(dtg, (W//2 - dtg.get_width()//2, py));         py += 30

    pygame.draw.line(screen, (50, 50, 70), (panel.x + 30, py), (panel.right - 30, py), 1)
    py += 14

    # rank based on score
    sc = game["score"]
    grade, gcol = ("S  RANK", YELLOW) if sc >= 50 else \
                  ("A  RANK", GREEN)  if sc >= 30 else \
                  ("B  RANK", BLUE)   if sc >= 15 else \
                  ("C  RANK", (180, 180, 180))
    gr = big.render(grade, True, gcol)
    screen.blit(gr, (W//2 - gr.get_width()//2, py));            py += 58

    if game.get("combo", 0) >= 3:
        cs = small.render(f"Best Combo : {game['combo']}", True, YELLOW)
        screen.blit(cs, (W//2 - cs.get_width()//2, py));        py += 26

    # play again / main menu buttons
    btn_y = panel.bottom + 20
    restart_r = pygame.Rect(W//2 - 185, btn_y, 170, 44)
    menu_r    = pygame.Rect(W//2 + 15,  btn_y, 170, 44)
    mouse     = pygame.mouse.get_pos()

    for r, label, col in [(restart_r, "PLAY AGAIN", GREEN), (menu_r, "MAIN MENU", (80,80,180))]:
        hov = r.collidepoint(mouse)
        c   = tuple(min(255, x + 40) for x in col) if hov else col
        pygame.draw.rect(screen, (0,0,0), r.move(3,3), border_radius=8)
        pygame.draw.rect(screen, c, r, border_radius=8)
        pygame.draw.rect(screen, WHITE, r, 1, border_radius=8)
        lbl = font.render(label, True, WHITE)
        screen.blit(lbl, (r.x + (r.w - lbl.get_width())//2,
                          r.y + (r.h - lbl.get_height())//2))

    hint = small.render("ENTER = Play Again     ESC = Menu", True, (80, 80, 80))
    screen.blit(hint, (W//2 - hint.get_width()//2, btn_y + 54))
