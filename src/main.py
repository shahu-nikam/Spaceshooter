import pygame, random, sys
pygame.init()
pygame.mixer.init()

from constants  import W, H, BLACK, WHITE, FPS, pwidth
from assets     import load_images, load_sounds, load_music, load_fonts
from scores     import load_scores
from game_state import reset
from gameplay   import build_enemy_types, update_game, _laser_beams
from screens    import (
    draw_menu, draw_difficulty, draw_results, draw_settings, draw_game_over,
    play, diff, setb, resb, easy, med, hard, ext, DIFF_COLORS
)

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Space Shooter")
clock  = pygame.time.Clock()

imgs        = load_images()
snd         = load_sounds()
fonts       = load_fonts()
enemy_types = build_enemy_types(imgs["enemy_images"])
load_music()

stars = [[random.randint(0, W), random.randint(0, H)] for _ in range(120)]

scores     = load_scores()
difficulty = "Medium"
pspeed     = 6
state      = "MENU"
game       = reset(pspeed)
float_texts= []
shield     = False
fire_time  = 0
over_timer = 0

settings = {"sound": True, "music": True, "volume": 0.7}
pygame.mixer.music.set_volume(settings["volume"])

btn_click = None
btn_timer = 0

menu_ship_x     = 100
menu_ship_speed = 2

def new_game():
    # wipes everything and gives us a clean game state for a fresh run
    global game, float_texts, shield, fire_time, over_timer
    _laser_beams.clear()
    game        = reset(pspeed)
    float_texts = []
    shield      = False
    fire_time   = 0
    over_timer  = 0

while True:
    clock.tick(FPS)
    screen.fill(BLACK)

    # starfield background
    for s in stars:
        b = 200 if state == "GAME" else 140
        pygame.draw.circle(screen, (b, b, b), (s[0], s[1]), 1)
        s[1] += 1
        if s[1] > H:
            s[0] = random.randint(0, W)
            s[1] = 0

    if btn_timer > 0: btn_timer -= 1
    else:             btn_click = None

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        # main menu clicks
        if state == "MENU" and e.type == pygame.MOUSEBUTTONDOWN:
            if   play.collidepoint(e.pos): btn_click=play; btn_timer=10; new_game(); state="GAME"
            elif diff.collidepoint(e.pos): btn_click=diff; btn_timer=10; state="DIFF"
            elif setb.collidepoint(e.pos): btn_click=setb; btn_timer=10; state="SET"
            elif resb.collidepoint(e.pos): btn_click=resb; btn_timer=10; state="RESULT"

        # difficulty screen clicks
        if state == "DIFF" and e.type == pygame.MOUSEBUTTONDOWN:
            for r, lbl in [(easy,"Easy"),(med,"Medium"),(hard,"Hard"),(ext,"Extreme")]:
                if r.collidepoint(e.pos):
                    btn_click=r; btn_timer=10; difficulty=lbl

        # game over - keyboard shortcuts
        if state == "OVER" and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN: new_game(); state="GAME"
            elif e.key == pygame.K_ESCAPE: over_timer=0; state="MENU"

        # game over - mouse clicks (only after the slide-in animation finishes)
        if state == "OVER" and e.type == pygame.MOUSEBUTTONDOWN and over_timer > 45:
            base_y = 155
            rr = pygame.Rect(W//2 - 185, base_y + 290 + 20, 170, 44)
            mr = pygame.Rect(W//2 + 15,  base_y + 290 + 20, 170, 44)
            if rr.collidepoint(e.pos): new_game(); state="GAME"
            elif mr.collidepoint(e.pos): over_timer=0; state="MENU"

        # settings screen shortcuts
        if state == "SET" and e.type == pygame.KEYDOWN:
            if e.key == pygame.K_s:
                settings["sound"] = not settings["sound"]
            if e.key == pygame.K_m:
                settings["music"] = not settings["music"]
                (pygame.mixer.music.unpause if settings["music"] else pygame.mixer.music.pause)()
            if e.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                settings["volume"] = round(max(0.0, settings["volume"] - 0.1), 1)
                pygame.mixer.music.set_volume(settings["volume"])
            if e.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                settings["volume"] = round(min(1.0, settings["volume"] + 0.1), 1)
                pygame.mixer.music.set_volume(settings["volume"])

        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE and state != "OVER":
            state = "MENU"

    # render whichever screen is active
    if state == "MENU":
        draw_menu(screen, fonts, difficulty, imgs["player"],
                  menu_ship_x, btn_click, btn_timer)
        menu_ship_x += menu_ship_speed
        if menu_ship_x > W - pwidth or menu_ship_x < 0:
            menu_ship_speed *= -1

    elif state == "DIFF":
        draw_difficulty(screen, fonts, difficulty, btn_click, btn_timer)

    elif state == "RESULT":
        draw_results(screen, fonts, scores)

    elif state == "SET":
        pspeed, settings = draw_settings(screen, fonts, pspeed, settings)

    elif state == "GAME":
        state, fire_time, shield, float_texts, scores = update_game(
            screen, game, state, difficulty, scores,
            snd, fonts, float_texts, shield,
            imgs, enemy_types, fire_time, settings
        )
        if state == "OVER":
            over_timer = 0

    elif state == "OVER":
        over_timer += 1
        draw_game_over(screen, fonts, game, scores, difficulty, over_timer)

    pygame.display.update()
