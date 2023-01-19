from src.core.population import Population


class Calibrator:

    POOL_SIZE = 100

    def __init__(self, input_labels, output_labels, driver, goal_score):
        self.population = Population(input_labels=input_labels, output_labels=output_labels)
        self.goal_score = goal_score
        
        self._monitors = []
        self.driver = driver

    def run(self):
        generation = 0
        
        self.population.init_random()
        current_population_copy = self.population.get_copy()
        
        while True:
            
            self.test_population(self.population)
            
            for copy, individual in zip(current_population_copy, self.population):
                individual.fitness = copy.fitness
            
            if self.is_goal_achieved(self.population):
                
                best_individuals = self.population.get_best_individuals()
                
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
                self.population.rebuild()

            generation += 1
    
    def is_goal_achieved(self, population):
        return any(individual.fitness >= self.goal_score for individual in population)

    def test_population(self, population):
        for individual in population:
            score = self.test_individual(individual)
            individual.set_fitness(score)
            
    def test_individual(self, individual):
        for input in self.driver.yield_input():
            output = individual.find_result(input)
            self.driver.send_output(output)

        return self.driver.read_result()
    
    def set_monitors(self, monitors):
        self._monitors = monitors