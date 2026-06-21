# assets.py
# loads images, sounds, music and fonts for the game
# paths are relative to the assets folder so this works on any pc, not just mine

import pygame
import os
from constants import enemy_size, pwidth, pheight

# go two levels up from src/ to project root, then into assets/
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_PATH      = os.path.join(BASE_DIR, "assets", "images", "img_png")
POWERUP_PATH  = os.path.join(BASE_DIR, "assets", "images", "powerup")
SOUND_PATH    = os.path.join(BASE_DIR, "assets", "sounds")


def load_images():
    # player ship
    player_img = pygame.image.load(os.path.join(IMG_PATH, "player.png")).convert_alpha()
    player_img = pygame.transform.scale(player_img, (pwidth, pheight))

    # 3 enemy types
    raw_enemies = [
        pygame.image.load(os.path.join(IMG_PATH, "enemy1.png")).convert_alpha(),
        pygame.image.load(os.path.join(IMG_PATH, "enemy2.png")).convert_alpha(),
        pygame.image.load(os.path.join(IMG_PATH, "enemy3.png")).convert_alpha(),
    ]
    enemy_images = [pygame.transform.scale(img, (enemy_size, enemy_size)) for img in raw_enemies]

    # powerup icons
    shield_img = pygame.image.load(os.path.join(POWERUP_PATH, "shield.png")).convert_alpha()
    shield_img = pygame.transform.scale(shield_img, (35, 35))

    laser_img = pygame.image.load(os.path.join(POWERUP_PATH, "laser.png")).convert_alpha()
    laser_img = pygame.transform.scale(laser_img, (35, 35))

    speed_img = pygame.image.load(os.path.join(POWERUP_PATH, "speed.png")).convert_alpha()
    speed_img = pygame.transform.scale(speed_img, (35, 35))

    return {
        "player":       player_img,
        "enemy_images": enemy_images,
        "shield":       shield_img,
        "laser":        laser_img,
        "speed":        speed_img,
    }


def load_sounds():
    return {
        "shoot":   pygame.mixer.Sound(os.path.join(SOUND_PATH, "shoot.wav")),
        "hit":     pygame.mixer.Sound(os.path.join(SOUND_PATH, "hit.wav")),
        "over":    pygame.mixer.Sound(os.path.join(SOUND_PATH, "gameover.wav")),
        "powerup": pygame.mixer.Sound(os.path.join(SOUND_PATH, "powerup.wav")),
    }


def load_music():
    pygame.mixer.music.load(os.path.join(SOUND_PATH, "bg.mp3"))
    pygame.mixer.music.play(-1)   # -1 = loop forever


def load_fonts():
    return {
        "font":  pygame.font.SysFont("arial", 26),
        "big":   pygame.font.SysFont("arial", 48),
        "small": pygame.font.SysFont("arial", 20),
    }
