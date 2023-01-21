import random
import time
import uuid
from src.core.constants import ALLOW_CREATE_BLOCK_TYPES, ALLOW_DELETE_BLOCK_TYPES, BLOCK_TYPE_TRANSMITTER
from src.core.cellular_automaton.map import Map

class Individual:

    DEFAULT_MAP_WIDTH = 8
    DEFAULT_MAP_HEIGHT = 8
    DEFAULT_BLOCKS_COUNT = 10
    MAP_UPDATE_ITERATION_COUNT = 20
    BLOCK_CREATE_MAX_COUNT = 5
    BLOCK_DELETE_MAX_COUNT = 5
    
    P_MUTATION_REPLACE_GEN = 0.3
    
    def __init__(self, input_labels=None, output_labels=None, genome=None, fitness=None):
        self.input_labels = input_labels
        self.output_labels = output_labels
        self.fitness = fitness
        self.id = uuid.uuid4()
        
        self.genome = genome or self.init_genome(input_labels, output_labels)
        self._monitors = []
        
    def __repr__(self):
        return str(self.id)

    def init_genome(self, input_labels, output_labels):
        genome = [
            Map(
                self.DEFAULT_MAP_WIDTH,
                self.DEFAULT_MAP_HEIGHT,
                input_labels,
                output_labels,
                main_output_label=output_label
            )
            for output_label in output_labels
        ]
        
        for gen in genome:
            gen.build_random_map(self.DEFAULT_BLOCKS_COUNT)
        
        return genome
    
    def find_result(self, input_set):
        self.__set_input(input_set)
        
        for index, gen in enumerate(self.genome):
            for _ in range(self.MAP_UPDATE_ITERATION_COUNT):
                
                for monitor in self._monitors:
                    monitor.render_map(index, gen)
                
                # input()

                update_count = gen.update_map_state()
                if update_count == 0:
                    break

        output = self.__build_genome_output()
        self.__reset_output()
        return output
    
    def __build_genome_output(self):
        return {gen.main_output_label: gen.get_main_output() for gen in self.genome}

    def mutate(self):
        if random.random() < self.P_MUTATION_REPLACE_GEN:
            self.replace_random_gen()
            
        else:
            gen = random.choice(self.genome)
            blocks_to_create_count = random.randint(1, self.BLOCK_CREATE_MAX_COUNT)
            blocks_to_delete_count = random.randint(1, self.BLOCK_DELETE_MAX_COUNT)
            
            can_add_blocks = gen.can_add_blocks(blocks_to_create_count)
            can_delete_blocks = gen.can_delete_blocks(blocks_to_delete_count)
            
            if can_add_blocks and can_delete_blocks:
                random_action = random.choice((True, False))
                
                if random_action:
                    gen.scatter_random_blocks(ALLOW_CREATE_BLOCK_TYPES, blocks_to_create_count)
                else:
                    gen.remove_random_blocks(ALLOW_DELETE_BLOCK_TYPES, blocks_to_delete_count)
                    
            elif can_add_blocks:
                gen.scatter_random_blocks(ALLOW_CREATE_BLOCK_TYPES, blocks_to_create_count)
            
            else:
                gen.remove_random_blocks(ALLOW_DELETE_BLOCK_TYPES, blocks_to_delete_count)

    def replace_random_gen(self):
        gen_index = random.choice(range(len(self.genome)))
        gen = self.genome[gen_index]
        new_genome = Map(
                self.DEFAULT_MAP_WIDTH,
                self.DEFAULT_MAP_HEIGHT,
                self.input_labels,
                self.output_labels,
                main_output_label=gen.main_output_label
            )
        
        new_genome.build_random_map(self.DEFAULT_BLOCKS_COUNT)
        self.genome[gen_index] = new_genome
    
    def get_copy(self):
        individual_copy = Individual(
            input_labels=self.input_labels,
            output_labels=self.output_labels,
            genome=self.get_genome_copy(),
            fitness=self.fitness,
        )
        individual_copy.set_monitors(self._monitors)
        return individual_copy
    
    def get_genome_copy(self):
        return [gen.get_copy() for gen in self.genome]
        
    def set_monitors(self, monitors):
        self._monitors = monitors

    def remove_monitors(self):
        self._monitors.clear()
        
    def set_fitness(self, fitness):
        self.fitness = fitness
        
    def __set_input(self, input_set):
        for gen in self.genome:
            gen.set_input(input_set)
            
    def __reset_output(self):
        for gen in self.genome:
            gen.reset_output()