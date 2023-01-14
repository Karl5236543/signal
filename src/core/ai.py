import random
import time
import uuid
from src.core.constants import ALLOW_CREATE_BLOCK_TYPES, ALLOW_DELETE_BLOCK_TYPES, BLOCK_TYPE_TRANSMITTER
from src.core.map import Map

class AI:

    DEFAULT_MAP_WIDTH = 10
    DEFAULT_MAP_HEIGHT = 10
    DEFAULT_BLOCKS_COUNT = 50 
    MAP_UPDATE_ITERATION_COUNT = 20
    BLOCK_CREATE_MAX_COUNT = 5
    BLOCK_DELETE_MAX_COUNT = 5

    def __init__(self, input_labels=None, output_labels=None, surface=None):
        
        self._map = surface or self.init_map(input_labels, output_labels)
        self._monitors = []

    def init_map(self, input_labels, output_labels):
        new_map = Map(self.DEFAULT_MAP_WIDTH, self.DEFAULT_MAP_HEIGHT, input_labels, output_labels)
        new_map.build_random_map(self.DEFAULT_BLOCKS_COUNT)
        return new_map

    def find_result(self, input_set):
        self._map.set_input(input_set)
        
        for count in range(self.MAP_UPDATE_ITERATION_COUNT):
            
            for monitor in self._monitors:
                monitor.render_map(1, self._map)
            
            # input()

            update_count = self._map.update_map_state()
            if update_count == 0:
                break

        output = self._map.get_output()
        self._map.reset_output()
        return output

    def mutate(self):
        
        blocks_to_create_count = random.randint(1, self.BLOCK_CREATE_MAX_COUNT)
        blocks_to_delete_count = random.randint(1, self.BLOCK_DELETE_MAX_COUNT)
        
        can_add_blocks = self._map.can_add_blocks(blocks_to_create_count)
        can_delete_blocks = self._map.can_delete_blocks(blocks_to_delete_count)
        
        if can_add_blocks and can_delete_blocks:
            random_action = random.choice((True, False))
            
            if random_action:
                self._map.scatter_random_blocks(ALLOW_CREATE_BLOCK_TYPES, blocks_to_create_count)
            else:
                self._map.remove_random_blocks(ALLOW_DELETE_BLOCK_TYPES, blocks_to_delete_count)
                
        elif can_add_blocks:
            self._map.scatter_random_blocks(ALLOW_CREATE_BLOCK_TYPES, blocks_to_create_count)
        
        else:
            self._map.remove_random_blocks(ALLOW_DELETE_BLOCK_TYPES, blocks_to_delete_count)

    def get_copy(self):
        ai = AI(
            input_labels=self._map.input_labels,
            output_labels=self._map.output_labels,
            surface=self._map.get_copy(),
        )
        ai.set_monitors(self._monitors)
        return ai
        
    def set_monitors(self, monitors):
        self._monitors = monitors

    def remove_monitors(self):
        self._monitors.clear()