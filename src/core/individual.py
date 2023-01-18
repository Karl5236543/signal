import random
import time
import uuid
from src.core.constants import ALLOW_CREATE_BLOCK_TYPES, ALLOW_DELETE_BLOCK_TYPES, BLOCK_TYPE_TRANSMITTER
from src.core.cellular_automaton.map import Map

class Individual:

    DEFAULT_MAP_WIDTH = 10
    DEFAULT_MAP_HEIGHT = 10
    DEFAULT_BLOCKS_COUNT = 50 
    MAP_UPDATE_ITERATION_COUNT = 20
    BLOCK_CREATE_MAX_COUNT = 5
    BLOCK_DELETE_MAX_COUNT = 5
    
    def __init__(self, input_labels=None, output_labels=None, genome=None):
        self._genome = genome or self.init_genome(input_labels, output_labels)
        self._fitness = None
        self._monitors = []

    def init_genome(self, input_labels, output_labels):
        genome = {
            Map(
                self.DEFAULT_MAP_WIDTH,
                self.DEFAULT_MAP_HEIGHT,
                input_labels,
                output_labels,
                main_output_label=output_label
            )
            for output_label in output_labels
        }
        
        for gen in genome:
            gen.build_random_map(self.DEFAULT_BLOCKS_COUNT)
        
        return genome
    
    def find_result(self, input_set):
        self.__set_input(input_set)
        
        for count in range(self.MAP_UPDATE_ITERATION_COUNT):
            
            for monitor in self._monitors:
                monitor.render_map(1, self._genome)
            
            # input()

            update_count = self._genome.update_map_state()
            if update_count == 0:
                break

        output = self.__build_genome_output()
        self.__reset_output()
        return output
    
    def __build_genome_output(self):
        return {gen.main_output_label: gen.get_main_output() for gen in self._genome}

    def mutate(self):
        # TODO:
        # можно создавать новые на замену случайному гену с некоторой вероятностью
        
        gen = random.choice(self._genome)
        
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

    def get_copy(self):
        individual_copy = Individual(
            input_labels=self._genome.input_labels,
            output_labels=self._genome.output_labels,
            genome=self._genome.get_copy(),
        )
        individual_copy.set_monitors(self._monitors)
        return individual_copy
        
    def set_monitors(self, monitors):
        self._monitors = monitors

    def remove_monitors(self):
        self._monitors.clear()
        
    def set_fitness(self, fitness):
        self._fitness = fitness
        
    def __set_input(self, input_set):
        for gen in self._genome:
            gen.set_input(input_set)
            
    def __reset_output(self):
        for gen in self._genome:
            gen.reset_output()