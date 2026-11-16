from dataclasses import dataclass

@dataclass(frozen=True)
class Pair:
    a_id: int
    b_id: int
    score: float

@dataclass(frozen=True)
class MatchResult:
    pairs: list[Pair]
    unmatched: list[int]

def allowed_pairs(participants):
    """Return the list of pairs (a_id, b_id) that pass the hard filter."""
    raise NotImplementedError


def select_pairs(pairs, scores):
    """Choose pairs so that the sum of their scores is as high as possible.

    Returns a list of Pair objects. Each participant appears in at most one pair.
    """
    raise NotImplementedError


def match(participants, scorer):
    """Match participants into pairs.

    participants: list of Participant
    scorer: function (participants, pairs) -> list of floats from 0 to 1,
        one score per pair, in the same order as pairs.
        It is provided from outside (random scorer in tests, language model later).

    Returns MatchResult with the chosen pairs and the ids of unmatched participants.
    """
    pairs = allowed_pairs(participants)
    scores = scorer(participants, pairs)
    chosen = select_pairs(pairs, scores)

    matched_ids = set()
    for pair in chosen:
        matched_ids.add(pair.a_id)
        matched_ids.add(pair.b_id)
    unmatched = [p.id for p in participants if p.id not in matched_ids]

    return MatchResult(pairs=chosen, unmatched=unmatched)
