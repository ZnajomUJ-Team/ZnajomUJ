from dataclasses import dataclass

@dataclass(frozen=True)
class Pair:
    a_id: int
    b_id: int
    score: float

ALGORITHM = "max_weight_matching v1"

@dataclass(frozen=True)
class MatchResult:
    pairs: list[Pair]
    unmatched: list[int]
    scorer: str
    algorithm: str

def allowed_pairs(participants):
    """Return the list of pairs (a_id, b_id) that pass the hard filter."""
    raise NotImplementedError


def select_pairs(scored_pairs):
    """Choose pairs so that the sum of their scores is as high as possible.

    Returns a list of Pair objects. Each participant appears in at most one pair.
    """
    raise NotImplementedError


def match(participants, scorer, scorer_name=None):
    """Match participants into pairs.

    participants: list of Participant
    scorer: function (participants, pairs) -> list of floats from 0 to 1,
        one score per pair, in the same order as pairs.
        It is provided from outside (random scorer in tests, language model later).
    scorer_name: text describing the scorer, e.g. model name and revision

    Returns MatchResult with the chosen pairs and the ids of unmatched participants.
    """
    if scorer_name is None: 
        scorer_name = scorer.__name__
    
    pairs = allowed_pairs(participants)
    scored_pairs = scorer(participants, pairs)
    chosen = select_pairs(scored_pairs)

    matched_ids = set()
    for pair in chosen:
        matched_ids.add(pair.a_id)
        matched_ids.add(pair.b_id)
    unmatched = [p.id for p in participants if p.id not in matched_ids]

    return MatchResult(pairs=chosen, unmatched=unmatched, scorer=scorer_name, algorithm=ALGORITHM)
