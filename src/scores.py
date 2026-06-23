import os
from constants import score_file

def load_scores():
    # default everything to 0 first, then overwrite from file if it exists
    scores = {"Easy": 0, "Medium": 0, "Hard": 0, "Extreme": 0}
    if os.path.exists(score_file):
        for line in open(score_file):
            line = line.strip()
            if not line or ":" not in line:
                continue   # skip blank/broken lines instead of crashing
            k, v = line.split(":")
            if k in scores:
                scores[k] = int(v)
    return scores


def save_scores(scores):
    with open(score_file, "w") as f:
        for k in scores:
            f.write(f"{k}:{scores[k]}\n")
