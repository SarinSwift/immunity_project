import random, sys
random.seed(42)
from person import Person
from logger import Logger
from Virus import Virus

class Simulation(object):

    def __init__(self, population_size, vacc_percentage, virus_name,
                 mortality_rate, basic_repro_num, initial_infected=1):
        self.population_size = population_size
        self.population = []
        self.total_infected = 0
        self.total_dead = 0
        self.current_infected = 0
        self.next_person_id = 0
        self.vacc_percentage = vacc_percentage
        self.virus_name = virus_name
        self.mortality_rate = mortality_rate
        self.virus = Virus(virus_name, mortality_rate, basic_repro_num)
        self.basic_repro_num = basic_repro_num
        self.initial_infected = initial_infected
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(
            virus_name, population_size, vacc_percentage, initial_infected)
        self.logger = Logger(self.file_name)
        self.logger.write_metadata(population_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num)

        self.newly_infected = []
        self._create_population(initial_infected)

    def _create_population(self, initial_infected):
        population = []
        infected_count = 0
        while len(population) < pop_size:
            if infected_count !=  initial_infected:
                infected_person_object = Person(self.next_person_id, False, self.virus)
                population.append(infected_person_object)
                infected_count += 1
                self.next_person_id += 1
            else:
                random_number = random.uniform(0, 1)
                if random_number < self.vacc_percentage:
                    healthy_person_vaccinated = Person(self.next_person_id, True, None)
                    population.append(healthy_person_vaccinated)
                    self.next_person_id += 1
                else:
                    healthy_person_not_vaccinated = Person(self.next_person_id, False, None)
                    population.append(healthy_person_not_vaccinated)
                    self.next_person_id += 1

        for person in population:
            self.population.append(person)

        self.current_infected = infected_count
        return population


    def _simulation_should_continue(self):
        dead = 0

        for person in self.population:
            if person.is_alive == False:
                print("person isnt alive")
                dead += 1
            elif person.infected != None and person.is_alive == True:
                self.total_infected += 1
                self.current_infected += 1
                return True
        else:
            if len(self.population) == 0 or self.current_infected == 0:
                print("everyone has died")
                return False
            else:
                return True

    def run(self):
        time_step_counter = 0
        should_continue = self._simulation_should_continue()
        while should_continue:
            self.time_step()
            time_step_counter += 1
            self.logger.log_time_step(time_step_counter)
            should_continue = self._simulation_should_continue()
        print('The simulation has ended after {} turns.'.format(time_step_counter))
        print("length of self.population is: {}".format(len(self.population)))
        print("current infected is: {}".format(self.current_infected))

    def time_step(self):
        for person in self.population:
            if person.infected != None and person.is_alive == True:
                interactions = 0
                deads = 0
                while interactions < 100:
                    randomized_person = random.choice(self.population)
                    if randomized_person.is_alive == True and person._id != randomized_person._id:
                        self.interaction(person, randomized_person)
                        interactions += 1
                    else:
                        deads += 1
                    if deads > len(self.population):
                        interactions = 100
                person.did_survive_infection()
                if person.did_survive_infection() == True:
                    self.logger.log_infection_survival(person, False)
                else:
                    self.logger.log_infection_survival(person, True)
                    self.total_dead += 1
                    self.population_size -= 1
                    self.population.remove(person)

        self._infect_newly_infected()

    def interaction(self, person, random_person):
        assert person.is_alive == True
        assert random_person.is_alive == True

        if random_person.infected == None and random_person.is_vaccinated == False:
            random_number = random.uniform(0, 1)
            if random_number < self.basic_repro_num:
                self.newly_infected.append(random_person._id)
                self.logger.log_interaction(person, random_person, True, False)
            else:
                self.logger.log_interaction(person, random_person, False, True)
        elif random_person.is_alive == False:
            self.logger.log_interaction(person, random_person, False, False)
        elif random_person.is_vaccinated == True:
            self.logger.log_interaction(person, random_person, False, True)
        elif random_person.infected != None:
            self.logger.log_interaction(person, random_person, False, False, self.virus)



    def _infect_newly_infected(self):
        just_infected = 0
        for id in self.newly_infected:
            for person in self.population:
                if person._id == id:
                    if person.is_alive == True and person.infected == None:
                        person.infected = self.virus
                        just_infected += 1
        self.total_infected += just_infected
        self.current_infected = just_infected
        self.newly_infected = []


if __name__ == "__main__":
    params = sys.argv[1:]
    pop_size = int(params[0])
    vacc_percentage = float(params[1])
    virus_name = str(params[2])
    mortality_rate = float(params[3])
    basic_repro_num = float(params[4])
    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1
    simulation = Simulation(pop_size, vacc_percentage, virus_name, mortality_rate,
                            basic_repro_num, initial_infected)
    simulation.run()


    # world = Simulation(20, 0.5, "HIV", 0.99, 0.25, 2)
    # world.run()
    # # print(world.population)
    #
    # infected_count = 0
    # for person in world.population:
    #         if person.infected is not None:
    #             infected_count += 1
    #
    # print(infected_count)
    # world._create_population(2)
    # print(len(world.population))
    # print(world.vacc_percentage == 0.5)
