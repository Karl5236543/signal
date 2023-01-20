

import random
from src.core.individual import Individual


class Population(list):
    
    TOURN_SIZE = 4
    P_CROSSOVER = 0.9
    P_MUTATION = 0.4

    def __init__(self, input_labels, output_labels, *args, **kwargs):
        self.input_labels = input_labels
        self.output_labels = output_labels
        super().__init__(*args, **kwargs)
    
    def rebuild(self):
        offspring = Population(
            self.input_labels,
            self.output_labels,
            self.sel_tournament()
        )
        
        offspring.crossover()

        self.clear()
        self.extend(offspring.get_copy())
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
    
    def sel_tournament(self):
        chosen = []
        for i in range(len(self)):
            aspirants = random.sample(self, k=self.TOURN_SIZE)
            chosen.append(max(aspirants, key=lambda indiv: indiv.fitness))
        return chosen
                
    def get_copy(self):
        return Population(self.input_labels, self.output_labels, [individual.get_copy() for individual in self])
    
    # def get_population_copy()
    
    def get_best_individuals(self):
        best_fitness = max(self, key=lambda indiv: indiv.fitness).fitness
        return [individual for individual in self if individual.fitness == best_fitness]
    
    def __cx_one_point(self, child1, child2):
        s = random.randint(2, len(child1.genome)-3)
        child1.genome[s:], child2.genome[s:] = child2.genome[s:], child1.genome[s:]
    
