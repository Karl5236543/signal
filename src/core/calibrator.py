

class Calibrator:

    SELECTED_COUNT = 3
    COPY_COUNT = 5
    POOL_SIZE = SELECTED_COUNT * COPY_COUNT

    def __init__(self, seed, driver, goal_score):
        self.id_counter = 0
        self.driver = driver
        self.base_seed = seed
        self.bot_pool = {}
        self._monitors = []
        self.goal_score = goal_score
    
    def rebuild_bot_pool(self, seeds):
        self.bot_pool.clear()
        self.id_counter = 0

        for seed in seeds:
            self.bot_pool[self.generate_id()] = seed

            for seed_copy in self.yield_copies(seed, self.COPY_COUNT - 1):
                seed_copy.mutate()
                self.bot_pool[self.generate_id()] = seed_copy
    
    def init_pool(self):
        for bot in self.yield_copies(self.base_seed, self.POOL_SIZE):
            self.bot_pool[self.generate_id()] = bot

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

        self.init_pool()
        
        while True:
            
            generation += 1
            pool_copies = {id: bot.get_copy() for (id, bot) in self.bot_pool.items()}
            
            for id, bot in self.bot_pool.items():
                score = self.run_test(bot)
                test_results[id] = score

            best_bot_ids = self.get_best_bots(test_results)
            best_bots_copies = [pool_copies[id] for id in best_bot_ids]

            self.rebuild_bot_pool(best_bots_copies)
            
            yield generation, [(pool_copies[id], test_results[id]) for bot in best_bot_ids]
            
            test_results.clear()
            if self.is_goal_achieved(test_results):
                break
            

    def generate_id(self):
        id = self.id_counter
        self.id_counter += 1
        return id
    
    def set_monitors(self, monitors):
        self._monitors = monitors