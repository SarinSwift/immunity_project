from person import Person
from Virus import Virus
import pytest
import io
import sys


def test_create_person():
    people = []
    person = Person(925, True)
    person2 = Person(926, True)
    people.append(person)
    people.append(person2)

    assert len(people) == 2
    assert people[0] == person
    assert people[1] == person2

def test_is_alive_and_is_vaccinated():
    virus = Virus("HIV", 0.8, 0.3)
    person = Person(925, True, virus)

    assert person._id == 925
    assert person.is_vaccinated == True
    assert person.infected == virus


def test_did_survive_infection():
    person = Person(925, True)
    person.did_survive_infection()
    assert True
