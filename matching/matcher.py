from dataclasses import dataclass
from itertools import combinations
import networkx as nx

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

def is_allowed(a, b):
    """Return True if a and b meet each other's hard criteria."""
    
    # age: each person must be within the other's preferred range
    if not (b.preferred_age_min <= a.age <= b.preferred_age_max):
        return False
    if not (a.preferred_age_min <= b.age <= a.preferred_age_max):
        return False

    # gender: "other" matches only the preference "any"
    if b.preferred_gender != "any" and a.gender != b.preferred_gender:
        return False
    if a.preferred_gender != "any" and b.gender != a.preferred_gender:
        return False

    # faculty: if either wants another faculty, they must differ
    if (a.other_faculty_only or b.other_faculty_only) and a.faculty == b.faculty:
        return False

    return True

def allowed_pairs(participants):
    """Return the list of pairs (a_id, b_id) that pass the hard filter."""
    pairs = []
    for a, b in combinations(participants, 2):
        if is_allowed(a, b):
            pairs.append((a.id,b.id))
    return pairs


def select_pairs(scored_pairs):
    """Choose pairs: first as many participants as possible, then the highest sum of scores.

    Returns a list of Pair objects. Each participant appears in at most one pair.
    """
    G = nx.Graph()
    for pair in scored_pairs:
        G.add_edge(pair.a_id, pair.b_id, weight=pair.score)
    matching = nx.max_weight_matching(G, maxcardinality=True)
    chosen = []
    for u, v in matching:
        score = G[u][v]["weight"]
        chosen.append(Pair(a_id=min(u, v), b_id=max(u, v), score=score))
    return chosen


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
