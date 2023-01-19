

import random
from src.core.individual import Individual
from deap.tools import selTournament


class Population(list):
    
    TOURN_SIZE = 3
    P_CROSSOVER = 0.9
    P_MUTATION = 0.1

    def __init__(self, input_labels, output_labels, *args, **kwargs):
        self.input_labels = input_labels
        self.output_labels = output_labels
        super().__init__(*args, **kwargs)
    
    def rebuild(self):
        offspring = Population(
            self.input_labels,
            self.output_labels,
            selTournament(self, len(self), self.TOURN_SIZE)
        )
        
        offspring.crossover()

        self.population = offspring.get_copy()
        self.mutate()

    def init_random(self, size):
        self.extend([Individual(self.input_labels, self.output_labels) for _ in range(size)])
    
    def crossover(self):
        for child1, child2 in zip(self[::2], self[1::2]):
            if random.random() < self.P_CROSSOVER:
                self.__cx_one_point(child1, child2)

    def mutate(self):
        for individual in self:
            if random.random() < self.P_MUTATION:
                individual.mutate()
                
    def get_copy(self):
        return Population(self.input_labels, self.output_labels, [individual.get_copy() for individual in self])
    
    # def get_population_copy()
    
    def get_best_individuals(self):
        best_fitness = max(self, key=lambda indiv: indiv.fitness).fitness
        return [individual for individual in self if individual.fitness == best_fitness]
    
    def __cx_one_point(self, child1, child2):
        s = random.randint(1, len(child1.genome)-2)
        child1.genome[s:], child2.genome[s:] = child2.genome[s:], child1.genome[s:]
    
