

from src.monitoring.bot_loader import BotDB


class Calibrator:

    SELECTED_COUNT = 1
    COPY_COUNT = 9
    POOL_SIZE = SELECTED_COUNT * (COPY_COUNT + 1)

    def __init__(self, seed, driver, goal_score):
        self.id_counter = 0
        self.driver = driver
        self.base_seed = seed
        self.population = {}
        self._monitors = []
        self.goal_score = goal_score
        self.db = BotDB()
    
    def rebuild_population(self, seeds):
        pass
        # TODO:
        # отбор
        # скрещивание
        # создание новой популяции
        
        # deprecated
        # self.population.clear()
        # self.id_counter = 0

        # for seed in seeds:
        #     self.population[f'{self.generate_id()}_main'] = seed

        #     for seed_copy in self.yield_copies(seed, self.COPY_COUNT):
        #         seed_copy.mutate()
        #         self.population[f'{self.generate_id()}_copy'] = seed_copy
    
    def init_pool(self):
        pass
        # TODO:
        # рандомно генерировать начальную популяцию (без использования сида)
        
        # deprecated
        # self.population[f'{self.generate_id()}_main'] = self.base_seed
        
        # for bot in self.yield_copies(self.base_seed, self.POOL_SIZE - 1):
        #     self.population[f'{self.generate_id()}_copy'] = bot

    def yield_copies(self, bot, count):
        for _ in range(count):
            yield bot.get_copy()

    def run_test(self, bot):
        for input in self.driver.yield_input():
            output = bot.find_result(input)
            self.driver.send_output(output)
        return self.driver.read_result()
    
    def get_best_bots(self, test_results):
        best_records = sorted(
            test_results.items(),
            key=lambda record: record[1],
            reverse=True
        )[:self.SELECTED_COUNT]

        return [record[0] for record in best_records]
    
    def is_goal_achieved(self, population):
        return any(result >= self.fitness for result in population.values())
    
    def test_population(self, population):
        for id, individual in self.population.items():
            score = self.run_test(individual)
            individual.set_fitness(score)

                
    
    def get_population_copy(self, population):
        return {id: individual.get_copy() for (id, individual) in self.population.items()}
    
    def run(self):
        generation = 0
        
        self.init_pool()
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
        best_fitness = max(self.population.values(), key=lambda indiv: indiv.fitness).fitness
        return [individual for individual in self.population.values() if individual.fitness == best_fitness]

    def generate_id(self):
        id = self.id_counter
        self.id_counter += 1
        return id
    
    def set_monitors(self, monitors):
        self._monitors = monitors