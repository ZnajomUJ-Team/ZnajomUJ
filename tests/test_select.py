from matching.generator import generate_participants
from matching.matcher import Pair, allowed_pairs, select_pairs
from matching.scoring import random_scorer


def test_prefers_more_people_over_higher_sum():
    scored = [
        Pair(1, 2, 0.1),
        Pair(2, 3, 0.9),
        Pair(3, 4, 0.1),
    ]
    result = select_pairs(scored)
    assert set(result) == {Pair(1, 2, 0.1), Pair(3, 4, 0.1)}
    
def test_no_people():
    scored = []
    result = select_pairs(scored)
    assert result == []

def test_only_one_pair():
    scored = [
        Pair(1, 2, 0.5),
    ]
    result = select_pairs(scored)
    assert result == [Pair(1, 2, 0.5)]
    
def test_prefers_higher_sum_if_amount_of_pairs_same():
    scored = [
        Pair(1, 2, 0.7),
        Pair(2, 3, 0.2),
        Pair(3, 4, 0.7),
        Pair(1, 4, 0.2),
    ]
    result = select_pairs(scored)
    assert set(result) == {Pair(1, 2, 0.7), Pair(3, 4, 0.7)}
    
def test_every_person_at_most_one_pair():
    participants = generate_participants(100, seed=1)
    pairs = allowed_pairs(participants)
    scored = random_scorer(participants, pairs)
    result = select_pairs(scored)
    ids = []
    for pair in result:
        ids.append(pair.a_id)
        ids.append(pair.b_id)
    assert len(ids) == len(set(ids))

def test_order_in_pair():
    scored = [
        Pair(2, 1, 0.5),
    ]
    result = select_pairs(scored)
    assert result == [Pair(1, 2, 0.5)]
    
