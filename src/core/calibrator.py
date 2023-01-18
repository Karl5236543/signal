

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
    
    def rebuild_bot_pool(self, seeds):
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
    
    def is_goal_achieved(self, test_results):
        return any(result >= self.goal_score for result in test_results.values())
    
    def run(self):
        generation = 0
        test_results = {}
        goal_achieved_counter = 0
        self.init_pool()
        
        while True:
            
            population_copy = {id: individual.get_copy() for (id, individual) in self.population.items()}
            
            for id, bot in self.population.items():
                score = self.run_test(bot)
                bot.set_fitness(score)
                
                # test_results[id] = score
                
                # if generation % 1000 == 0:
                #     print(f'gen_{generation}_res_{score}_{id}')
                # #     self.db.save_bot(f'gen_{generation}_res_{score}_{id}', bot)
                
            # best_bot_ids = self.get_best_bots(test_results)
            # best_bots_copies = [population_copy[id] for id in best_bot_ids]
            
            if self.is_goal_achieved(test_results):
                goal_achieved_counter += 1
                
                if goal_achieved_counter > 100:
                    return self.get_best_individual()
                
                self.population = best_bots_copies
                
            else:
                goal_achieved_counter = 0
                self.rebuild_bot_pool(best_bots_copies)

            test_results.clear()
            generation += 1

    def get_best_individual(self):
        return max(self.population.values(), key=lambda indiv: indiv.fitness)

    def generate_id(self):
        id = self.id_counter
        self.id_counter += 1
        return id
    
    def set_monitors(self, monitors):
        self._monitors = monitors