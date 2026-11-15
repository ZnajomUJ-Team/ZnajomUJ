import random

from matching.participants import Participant

def generate_participants(n: int, seed: int = 0) -> list[Participant]:
    rng = random.Random(seed)
    participants = []
    for i  in range(n):
        g = rng.choices(["woman", "man", "other"], weights = [50, 45, 5])[0]
        a = round(rng.triangular(18,30,20))
        f = rng.choice(["WPiA", "WL", "WF", "WNoZ", "WFz", "WH", "WFil", "WP", "WFAIS", "WMI", "WCh", "WB", "WZiKS", "WSMiP", "WBBiB"])
        pg = rng.choices(["woman", "man", "any"], weights = [30, 20, 50])[0]
        pamin = max(18, a - rng.randint(1, 4))
        pamax = min(30, a + rng.randint(1, 5))
        ofo = rng.random() < 0.3
        participants.append(Participant(
            id=i,
            gender=g,
            age=a,
            faculty=f,
            preferred_gender=pg,
            preferred_age_min=pamin,
            preferred_age_max=pamax,
            other_faculty_only=ofo,
        ))
    return participants
