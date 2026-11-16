import random

def random_scorer(participants, pairs, seed=0):
    """Return a random score from 0 to 1 for each pair. For tests only."""
    scores = []
    rng = random.Random(seed)
    for _ in pairs:
        i = rng.random()
        scores.append(i)
    return scores
