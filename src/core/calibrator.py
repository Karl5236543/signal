

from src.core.individual import Individual
from src.monitoring.bot_loader import BotDB
from deap import tools

tools.selTournament
tools.cxOnePoint

class Calibrator:

    POOL_SIZE = 100

    def __init__(self, input_labels, output_labels, driver, goal_score):
        self.id_counter = 0
        self.driver = driver
        self.population = []
        self._monitors = []
        self.goal_score = goal_score
        self.db = BotDB()
        
        self.input_labels = input_labels 
        self.output_labels = output_labels
    
    def rebuild_population(self):
        
        
        # TODO:
        
        # отбор
        # selTournament
        
        # скрещивание
        # cxOnePoint
        
        # создание новой популяции
        
        # deprecated
        # self.population.clear()
        # self.id_counter = 0

        # for seed in seeds:
        #     self.population[f'{self.generate_id()}_main'] = seed

        #     for seed_copy in self.yield_copies(seed, self.COPY_COUNT):
        #         seed_copy.mutate()
        #         self.population[f'{self.generate_id()}_copy'] = seed_copy
    
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