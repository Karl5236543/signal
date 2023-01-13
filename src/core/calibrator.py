

class Calibrator:

    SELECTED_COUNT = 1
    COPY_COUNT = 5
    EXACT_COPIES_COUNT = 1

    def __init__(self, seed, driver):
        self.id_counter = 0
        self.driver = driver
        self.base_seed = seed
        self.seed_pool = self.init_pool()
        self.seed_result = {}
        self._monitors = []
        
    def init_pool(self):
        seed_pool = {}
        for seed in self.yield_copies(self.base_seed, self.SELECTED_COUNT * self.COPY_COUNT):
            seed_pool[self.generate_id()] = seed
        return seed_pool

    def yield_copies(self, seed, count):
        for _ in range(count):
            yield seed.get_copy()

    def run_test(self, seed):
        for input in self.driver.yield_input():
            output = seed.find_result(input)
            self.driver.send_output(output)
        
        return self.driver.read_result()
    
    # TODO:
    # делать копии объектов в начальном состоянии (до начала подачи инпутов (до run_test))
    def run(self):
        while True:
            for id, ai in self.seed_pool.items():
                score = self.run_test(ai)
                self.seed_result[id] = score

            results = self.seed_result.items()
            best_records = sorted(results, key=lambda record: record[1], reverse=True)[:self.SELECTED_COUNT]
            
            # best_records = (
            #     sorted(
            #         self.seed_result.items(),
            #         key=lambda id, score: score,
            #         reverse=True)
            #     )[:self.SELECTED_COUNT]

            result = [score for (_, score) in best_records]

            ais = [self.seed_pool[id] for (id, _) in best_records]

            self.rebuild_ai_pool(ais)
            self.seed_result.clear()
            
            yield result

    def rebuild_ai_pool(self, seeds):
        self.seed_pool.clear()
        self.id_counter = 0
        for seed in seeds:
            for index, seed_copy in enumerate(self.yield_copies(seed, self.COPY_COUNT)):
                if index > self.EXACT_COPIES_COUNT:
                    seed_copy.mutate()
                self.seed_pool[self.generate_id()] = seed_copy

    def generate_id(self):
        id = self.id_counter
        self.id_counter += 1
        return id
    
    def set_monitors(self, monitors):
        self._monitors = monitors