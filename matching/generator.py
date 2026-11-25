import random

from matching.participants import Participant

FACULTIES = ["WPiA", "WL", "WF", "WNoZ", "WFz", "WH", "WFil", "WP",
             "WFAIS", "WMI", "WCh", "WB", "WZiKS", "WSMiP", "WBBiB"]

def generate_participants(n: int, seed: int = 0) -> list[Participant]:
    rng = random.Random(seed)
    participants = []
    for i  in range(n):
        gender = rng.choices(["woman", "man", "other"], weights = [50, 45, 5])[0]
        age = round(rng.triangular(18,30,20))
        faculty = rng.choice(FACULTIES)
        preferred_gender = rng.choices(["woman", "man", "any"], weights = [30, 20, 50])[0]
        preferred_age_min = max(18, age - rng.randint(1, 4))
        preferred_age_max = min(30, age + rng.randint(1, 5))
        other_faculty_only = rng.random() < 0.3
        participants.append(Participant(
            id=i,
            gender=gender,
            age=age,
            faculty=faculty,
            preferred_gender=preferred_gender,
            preferred_age_min=preferred_age_min,
            preferred_age_max=preferred_age_max,
            other_faculty_only=other_faculty_only,
        ))
    return participants
