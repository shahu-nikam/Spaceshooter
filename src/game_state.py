# game_state.py
# holds the function that gives us a fresh game state every time we restart

from constants import W, pwidth, H

def reset(pspeed_val=6):
    return {
        "px":                  W // 2 - pwidth // 2,
        "py":                  H - 80,
        "bullets":             [],
        "enemies":             [],
        "score":               0,
        "powerup_timer":       0,
        "powerup_spawn_timer": 0,
        "powerup_next":        300,
        "timer":               0,
        "combo":               0,
        "lives":               3,
        "powerups":            [],
        "new_record":          False,
        "laser_powerup":       False,
        "pspeed":              pspeed_val,
    }
