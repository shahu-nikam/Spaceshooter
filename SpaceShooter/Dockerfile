# Dockerfile — Space Shooter (desktop pygame version)
#
# NOTE: pygame needs a real display/window to actually play the game.
# A normal Docker container has no screen, so this image is only meant
# for checking that the code, imports, and dependencies all work
# (syntax check / import smoke test) - it will NOT show the actual
# game window. If you want the real game with graphics, just run
# run_game.py directly on your own machine.

FROM python:3.10-slim

# SDL (which pygame uses under the hood) needs a couple of system
# libraries even in headless mode, plus libs for image/audio decoding
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    libjpeg62-turbo \
    libpng16-16 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# install pygame
RUN pip install --no-cache-dir pygame

# copy the project in
COPY . .

# force SDL into headless/dummy mode so pygame.init() and
# pygame.display.set_mode() don't crash without a real screen
ENV SDL_VIDEODRIVER=dummy
ENV SDL_AUDIODRIVER=dummy

# quick smoke test on build: makes sure every module imports cleanly.
# image loading is skipped here since your actual PNG files need to be
# added to assets/images/ first - this just checks the code itself runs
RUN python -c "\
import sys; sys.path.insert(0, 'src'); \
import pygame; pygame.init(); pygame.display.set_mode((800,600)); pygame.mixer.init(); \
import assets, scores, game_state, gameplay, screens, draw_utils, constants; \
print('All modules imported successfully.'); \
print(scores.load_scores()); \
print(game_state.reset(6)); \
print('Smoke test passed - code is structurally sound.')"

CMD ["python", "run_game.py"]
