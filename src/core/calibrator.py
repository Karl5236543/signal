

import random
from src.core.individual import Individual
from src.monitoring.bot_loader import BotDB
from deap.tools import selTournament


class Population(list):
    
    TOURN_SIZE = 3
    P_CROSSOVER = 0.9
    P_MUTATION = 0.1
    
    


class Calibrator:

    POOL_SIZE = 100
    TOURN_SIZE = 3
    
    P_CROSSOVER = 0.9
    P_MUTATION = 0.1

    def __init__(self, input_labels, output_labels, driver, goal_score):
        self.population = []
        self._monitors = []
        self.driver = driver
        self.goal_score = goal_score
        self.input_labels = input_labels 
        self.output_labels = output_labels
    
    def rebuild_population(self):
        offspring = selTournament(self.population, self.POOL_SIZE, self.TOURN_SIZE)
        self.crossover(offspring)

        self.population = self.get_population_copy(offspring)
        self.mutate_population()
    
    def crossover(self, offspring):
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < self.P_CROSSOVER:
                self.cx_one_point(child1, child2)
                
    def cx_one_point(self, child1, child2):
        s = random.randint(2, len(child1)-3)
        child1.genome[s:], child2.genome[s:] = child2.genome[s:], child1.genome[s:]
        
    def mutate_population(self):
        for individual in self.population:
            if random.random() < self.P_MUTATION:
                individual.mutate()
    
    def init_population(self):
        self.population = [Individual(self.input_labels, self.output_labels) for _ in range(self.POOL_SIZE)]

    def run_test(self, bot):
        for input in self.driver.yield_input():
            output = bot.find_result(input)
            self.driver.send_output(output)

        return self.driver.read_result()
    
    def is_goal_achieved(self, population):
        return any(individual.fitness >= self.goal_score for individual in population)
    
    def test_population(self, population):
        for individual in population:
            score = self.run_test(individual)
            individual.set_fitness(score)
    
    def get_population_copy(self, population):
        return [individual.get_copy() for individual in self.population]
    
    def run(self):
        generation = 0
        
        self.init_population()
        current_population_copy = self.get_population_copy(self.population)
        
        while True:
            self.test_population(current_population_copy)
            
            for copy, individual in zip(current_population_copy, self.population):
                individual.fitness = copy.fitness
            
            if self.is_goal_achieved(self.population):
                
                best_individuals = self.get_best_individuals()
                
                for individual in best_individuals:
                    goal_achieved_counter = 0
                    
                    while True:
                        individual_copy = individual.get_copy()
                        
                        self.test_population([individual_copy])
                        
                        if self.is_goal_achieved([individual_copy]):
                            goal_achieved_counter += 1

                            if goal_achieved_counter == 50:
                                individual.fitness = individual_copy.fitness
                                return individual
                            
                        else:
                            break
                
            else:
                self.rebuild_population()

            generation += 1

    def get_best_individuals(self):
        best_fitness = max(self.population, key=lambda indiv: indiv.fitness).fitness
        return [individual for individual in self.population if individual.fitness == best_fitness]

    def generate_id(self):
        id = self.id_counter
        self.id_counter += 1
        return id
    
    def set_monitors(self, monitors):
        self._monitors = monitors