from person import Person
from Virus import Virus

class Logger(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       basic_repro_num):
        file = open(self.file_name, 'w')
        file.write("population size:{}\nvaccine percentage:{}\nvirus name:{}\nmortality rate:{}\nbasic reproduction number:{}\n".format(str(pop_size), str(vacc_percentage), str(virus_name), str(mortality_rate), str(basic_repro_num)))
        file.close()


    def log_interaction(self, person1, person2, did_infect=None,
                        person2_vacc=None, person2_sick=None):
        file = open(self.file_name, 'a')
        if did_infect == True:
            file.write("\n{} infects {}\n".format(person1._id, person2._id))
        elif did_infect == False:
            file.write("\n{} didn't infect {} because is already vaccinated or already sick.\n".format(person1._id, person2._id))
        file.close()


    def log_infection_survival(self, person, did_die_from_infection):
        file = open(self.file_name, 'a')
        if did_die_from_infection == False:
            file.write("{} survived infection\n".format(person._id))
        else:
            file.write("{} died from infection\n".format(person._id))
        file.close()

    def log_time_step(self, time_step_number):
        file = open(self.file_name, 'a')
        new_time_step_counter = time_step_number + 1
        file.write("Time step {} ended, beginning time step {}\n\n".format(time_step_number, new_time_step_counter))
        file.close()

# if __name__ == "__main__":
#     logger = Logger('first_log')
#     logger.write_metadata(100, 0.5, "ebola", 0.7, 0.3)
#
#     ebola = Virus("Ebola", 0.8, 0.25)
#     sarin = Person(22, True, ebola)
#     rinni = Person(23, False)
#     logger.log_interaction(sarin, rinni, True, False, False)
#
#     logger.log_infection_survival(rinni, True)
#
#     logger.log_time_step(1)
