from dataclasses import dataclass

@dataclass(frozen=True)
class Participant:
    id: int
    gender: str               # "woman", "man", "other"
    age: int
    faculty: str
    preferred_gender: str     # "woman", "man", "any"
    preferred_age_min: int
    preferred_age_max: int
    other_faculty_only: bool
    answers: tuple[str, ...] = ()
