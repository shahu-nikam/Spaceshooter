"""
run_game.py — start the game from the project root

just run:  python run_game.py
(this adds src/ to the path so the internal imports keep working)
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import main  # noqa: triggers the game loop on import
