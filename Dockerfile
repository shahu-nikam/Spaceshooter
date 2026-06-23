FROM python:3.10-slim


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


RUN python -c "\
import sys; sys.path.insert(0, 'src'); \
import pygame; pygame.init(); pygame.display.set_mode((800,600)); pygame.mixer.init(); \
import assets, scores, game_state, gameplay, screens, draw_utils, constants; \
print('All modules imported successfully.'); \
print(scores.load_scores()); \
print(game_state.reset(6)); \
print('Smoke test passed - code is structurally sound.')"

CMD ["python", "run_game.py"]
