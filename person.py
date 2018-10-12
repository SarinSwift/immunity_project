import random
random.seed(42)
# TODO: Import the virus clase
from Virus import Virus

class Person(object):

    def __init__(self, _id, is_vaccinated, infected=None):
        self.alive = True
        self._id = _id
        self.is_vaccinated = is_vaccinated
        self.infected = infected
        self.is_alive = True
        self.infection = infected


    def did_survive_infection(self, mortality_rate):
        if self.infection != None:
            random_number =  random.uniform(0, 1)
            if random_number < self.infected.mortality_rate:
                self.is_alive = False
                return False
            else:
                self.is_vaccinated = True
                self.infected = None
                return True



# if __name__ == "__main__":
#     ebola = Virus("Ebola", 0.8, 0.25)
#     sarin = Person(22, True, ebola)
#
#     print(sarin.alive == True)
#     print(sarin.infected == ebola)
#     print(sarin.infected.mortality_rate)
