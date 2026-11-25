import random
from matching.matcher import Pair

def random_scorer(participants, pairs, seed=0):
    """Return a Pair with a random score from 0 to 1 for each pair. For tests only."""
    scored_pairs = []
    rng = random.Random(seed)
    for a_id, b_id in pairs:
        score = rng.random()
        scored_pairs.append(Pair(a_id=a_id, b_id=b_id, score=score))
    return scored_pairs
