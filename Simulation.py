import random, sys
from Person import Person
from Virus import Virus
from FileWriter import FileWriter

class Simulation:
  
    def __init__(self, initial_vaccinated, initial_infected, initial_healthy, virus, resultsfilename):
        '''Set up the initial simulation values'''

        self.virus = virus 

        self.initial_infected = initial_infected 
        self.total_infected = 0
        self.current_infected = 0
        self.newly_infected = []
        self.number_infected = 0

        self.initial_healthy = initial_healthy
        self.initial_vaccinated = initial_vaccinated

        self.population = []

        self.population_size = initial_infected + initial_healthy + initial_vaccinated


        self.total_dead = 0
        self.newly_dead = 0
        self.total_vaccinated = initial_vaccinated

        self.file_writer = FileWriter(resultsfilename)


    def create_population(self):
        '''Creates the population (a list of Person objects) consisting of initial infected people, initial healthy non-vaccinated people, and 
        initial healthy vaccinated people. Adds them to the population list'''

        for i in range(self.initial_infected):
        	person = Person(False, virus)
        	self.population.append(person)

        for i in range(self.initial_healthy):
            person = Person(False, None)
            self.population.append(person)

        for i in range(self.initial_vaccinated):
            person = Person(True, None)
            self.population.append(person)
        	
    # def print_population(self):
    #     '''Prints out every person in the population and their current attributes'''
    #     for person in self.population:
    #         print (person, self.initial_infected,self.initial_healthy,self.initial_vaccinated)


    # def get_infected(self):
    #     '''Gets all the infected people from the population and returns them as a list'''
    #     # for i in range(self.initial_infected):
    #     #     person = Person(True,1)
    #     #     self.population.append(person)
    #     number_of_infected = self.initial_infected
        

    def simulation_should_continue(self):
        '''Determines whether the simulation should continue.
        If everyone in the population is dead then return False, the simulation should not continue
        If everyone in the population is vaccinated return False
        If there are no more infected people left and everyone is either vaccinated or dead return False
        In all other cases return True'''
        #check if total dead is the same length of population
        if self.total_dead == len(self.population):
            return False
        #check if all population are vaccinated
        elif self.initial_vaccinated == len(self.population):
            return False
        else:
            return True



    def run(self):
        ''' This method should run the simulation until all requirements for ending
        the simulation are met.
        '''
        print(f"--- Simulation Begins ---")
        time_step_counter = 0
        should_continue = self.simulation_should_continue()
        while should_continue:
        
            self.time_step()
            self._infect_newly_infected()
            self.file_writer.init_file(self.virus, self.population_size, self.initial_vaccinated, self.initial_healthy, self.initial_infected)
            should_continue = self._simulation_should_continue()

        print(f'The simulation has ended after {time_step_counter} turns.')
        self.file_writer.write_results(time_step_counter, self.total_dead, self.total_vaccinated)
            

    def time_step(self, infected):
        ''' For every infected person interact with a random person from the population 10 times'''
        #TODO: get a random index for the population list
        #TODO: using the random index get a random person from the population
        #TODO: call interaction() with the current infected person and the random person

        self.newly_infected = []
        self.newly_dead = 0
        self.number_infected = 0
        for person in self.population:

            if not person.infection == None:
                self.number_infected += 1
                live_population_without_person = [] # People can't interact with themselves or dead people
                for other_person in self.population:
                    if not other_person._id == person._id and other_person.is_alive == True:
                        live_population_without_person.append(other_person)
                self.interaction(person, random.sample(live_population_without_person, 100))
                random_person = random.uniform(0,1)

                if random_person <= self.virus.mortality_rate:
                    person.infection = None
                    person.is_alive = False
                    self.newly_dead += 1
                    self.file_writer_infection(person,True)
                else:
                    person.is_vaccinated = True
                    person.infection = None
                    self.file_writer_infection_survival(person,False)
        self.total_dead += self.newly_dead
        self.total_infected += len(self.newly_infected)

            

    #def interaction(self, infected, random_person):

    def interaction(self, person, random_people_list):
        for random_person in random_people_list:
            if random_person.is_vaccinated == False:
                if random_person.infection == None and random_person not in self.newly_infected: # If they're healthy but unvaccinated
                    dice_roll = random.uniform(0,1)
                    if dice_roll <= self.virus.repro_rate:
                        self.newly_infected.append(random_person)
                        self.file_writer_interaction(person, random_person, False,False,True)
                    else:
                        self.file_writer_interaction(person,random_person,False,False,False)
                else:
                    self.file_writer_interaction(person, random_person, True, False, False)
                assert person.is_alive == True
                assert random_person.is_alive == True
            else:
                self.file_writer_interaction(person, random_person, False, True, False)

        



if __name__ == "__main__":

    #Set up the initial simulations values
    virus_name = "Malaise"
    reproduction_num = 0.20
    mortality_num = .99

    initial_healthy = 10
    initial_vaccinated = 5

    initial_infected = 1

    virus = Virus(virus_name, reproduction_num, mortality_num)

    simulation = Simulation(initial_vaccinated, initial_infected, initial_healthy, virus, "results.txt")

    #run the simulation
    simulation.run()