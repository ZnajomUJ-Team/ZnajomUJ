from matching.matcher import is_allowed
from matching.participants import Participant


def person(id, gender="woman", age=21, faculty="WMI", preferred_gender="any",
           age_min=18, age_max=30, other_faculty_only=False):
    return Participant(id, gender, age, faculty, preferred_gender,
                       age_min, age_max, other_faculty_only)


def test_same_faculty_allowed_when_nobody_minds():
    assert is_allowed(person(1), person(2))

def test_same_faculty_rejected_when_one_wants_another():
    assert not is_allowed(person(1, other_faculty_only=True), person(2))

def test_different_faculty_allowed_when_one_wants_another():
    assert is_allowed(person(1, faculty="WMI", other_faculty_only=True), person(2, faculty="WCh"))
    
def test_age_in_preferred_range():
    assert is_allowed(person(1, age_min=20, age_max=24), person(2, age=22))

def test_age_is_smaller_than_preferred():
    assert not is_allowed(person(1, age_min=25), person(2))

def test_age_is_larger_than_preferred():
    assert not is_allowed(person(1, age_max=20), person(2))

def test_age_on_range_boundaries_is_allowed():
    assert is_allowed(person(1, age_min=21, age_max=21), person(2, age=21))
    
def test_any_gender_preferred():
    assert is_allowed(person(1), person(2))

def test_one_gender_preferration():
    assert not is_allowed(person(1, preferred_gender="man"), person(2))

def test_two_gender_preferration():
    assert not is_allowed(person(1, preferred_gender="woman"), person(2, preferred_gender="man"))

def test_other_gender_allowed_only_with_any_preference():
    other = person(1, gender="other")
    assert is_allowed(other, person(2, preferred_gender="any"))
    assert not is_allowed(other, person(2, preferred_gender="woman"))
    assert not is_allowed(other, person(2, preferred_gender="man"))

def test_specific_gender_preference_met():
    assert is_allowed(person(1, preferred_gender="woman"), person(2, gender="woman"))

def test_order_does_not_matter():
    a = person(1, preferred_gender="man")
    b = person(2, gender="man", age=25)
    assert is_allowed(a, b) == is_allowed(b, a)
