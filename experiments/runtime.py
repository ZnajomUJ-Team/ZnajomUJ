import time

from matching.generator import generate_participants
from matching.matcher import allowed_pairs, select_pairs
from matching.scoring import random_scorer

SIZES = [100, 300, 1000, 2000, 3000]


def run(n):
    """Measure each matching stage for n generated participants."""
    participants = generate_participants(n, seed=1)

    start = time.perf_counter()
    pairs = allowed_pairs(participants)
    filter_time = time.perf_counter() - start

    start = time.perf_counter()
    scored = random_scorer(participants, pairs)
    scorer_time = time.perf_counter() - start

    start = time.perf_counter()
    chosen = select_pairs(scored)
    select_time = time.perf_counter() - start

    print(n, len(pairs), len(chosen),
          round(filter_time, 2), round(scorer_time, 2), round(select_time, 2))


def main():
    print("osoby | dozwolone pary | wybrane pary | filtr [s] | scorer [s] | dobieranie [s]")
    for n in SIZES:
        run(n)


if __name__ == "__main__":
    main()
