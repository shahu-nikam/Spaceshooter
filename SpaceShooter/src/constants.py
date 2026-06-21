# constants.py
# all the fixed values used across the game - screen size, colors, speeds etc

# screen size
W, H = 800, 600

# colors (RGB)
BLACK  = (0,   0,   0  )
WHITE  = (255, 255, 255)
RED    = (255, 50,  50 )
GREEN  = (50,  255, 50 )
BLUE   = (50,  150, 255)
YELLOW = (255, 215, 0  )

FPS = 60

# player
pwidth, pheight = 60, 20
MIN_SPEED, MAX_SPEED = 2, 12

# bullets
bullet_speed = 8
fire_gap     = 10   # frames between shots

# enemy size
enemy_size = 65

# difficulty settings - spawn = lower means faster spawn rate
diff_data = {
    "Easy":    {"speed": 2, "spawn": 60, "mult": 1},
    "Medium":  {"speed": 3, "spawn": 40, "mult": 1},
    "Hard":    {"speed": 4, "spawn": 30, "mult": 2},
    "Extreme": {"speed": 6, "spawn": 20, "mult": 3},
}

# keeps scores.txt in the project root no matter where the game is launched from
import os
score_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scores.txt")
