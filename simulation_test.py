from person import Person
from simulation import Simulation
from Virus import Virus
from logger import Logger
import pytest
import random

def test_initialize_simulation():
    thailand = Simulation(100, 0.3, "malaria", 0.5, 0.2)
    singapore = Simulation(1000, 0.5, "dengue", 0.3, 0.7)

    assert thailand.population_size == 100
    assert singapore.initial_infected == 1

def test_create_population():
    thailand = Simulation(100, 0.3, "malaria", 0.5, 0.2)
    thailand._create_population(1)
    assert len(thailand.population) == 100

    # checks for the correct infected count person
    infected_count = 0
    for person in thailand.population:
        if person.infected != None:
            infected_count += 1
    assert infected_count == 1


def test_simulation_should_continue():
    thailand = Simulation(100, 0.3, "malaria", 0.5, 0.2)
    thailand._create_population(1)
    # if everyone is dead, it should not continue
    for person in thailand.population:
        person.is_alive = False
    assert thailand._simulation_should_continue() == False

    # if lenght of population is 0, it should not continue
    for person in thailand.population:
        thailand.population.remove(person)
    assert thailand._simulation_should_continue() == False

    # if everyone's alive and vaccinated and has no infection, it should not continue
    for person in thailand.population:
        person.is_alive = True
        person.is_vaccinated = True
        person.infected = None
    assert thailand._simulation_should_continue() == False


def test_infect_newly_infected():
    # Checks to see if it had emptied the list or not
    thailand = Simulation(100, 0.3, "malaria", 0.5, 0.2)
    thailand._create_population(1)
    thailand.newly_infected = [0, 1, 2, 3]
    thailand._infect_newly_infected()
    assert len(thailand.newly_infected) == 0

    # makes sure all the people in newly_infected has a virus
    ids = [0, 1, 2, 3]
    thailand.newly_infected = ids
    thailand._infect_newly_infected()
    for id in ids:
        for person in thailand.population:
            if person._id == id:
                assert person.infected != None

def test_interaction():
    small_land = Simulation(10, 0.3, "Ebola", 0.5, 0.2, 3)
    small_land._create_population(3)

    interactions = 1
    for person in small_land.population:
        while interactions < 100:
            randomized_person = random.choice(small_land.population)
            if randomized_person.is_alive == True and person._id != randomized_person._id:
                small_land.interaction(person, randomized_person)
                assert person._id != randomized_person._id
                assert randomized_person.is_alive == True
                interactions += 1
        assert interactions == 100
