# virus_test.py
from Virus import Virus
import pytest

def test_initialize_virus():
    virus_object = Virus("HIV", 0.3, 0.8)
    assert virus_object.name == "HIV"
    assert virus_object.mortality_rate == 0.3
    assert virus_object.repro_rate == 0.8
