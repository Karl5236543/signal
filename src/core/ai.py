import random
from core.constants import ALLOW_CREATE_BLOCK_TYPES, ALLOW_DELETE_BLOCK_TYPES, BLOCK_TYPE_TRANSMITTER
from core.map import Map

class AI:

    MAP_WIDTH = 50
    MAP_HEIGHT = 50
    BLOCKS_COUNT = 300
    MAP_UPDATE_ITERATION_COUNT = 250
    BLOCK_CREATE_MAX_COUNT = 5
    BLOCK_DELETE_MAX_COUNT = 5

    def __init__(self, input_labels, output_labels, map=None):
        self.input_labels = input_labels
        self.output_labels = output_labels
        self._map = map or self.init_map(self.input_labels, self.output_labels)

    def init_map(self, input_labels, output_labels):
        new_map = Map(self.MAP_WIDTH, self.MAP_HEIGHT)
        new_map.build_random_map(input_labels, output_labels, self.BLOCKS_COUNT)
        return new_map

    def find_result(self, input):
        self._map.set_input(input)
        
        for _ in range(self.MAP_UPDATE_ITERATION_COUNT):
            self._map.update_map_state()
            self._monitor.render(self._map)
        
        output = self._map.get_output()
        self._map.reset_output()
        return output

    def mutate(self):
        
        blocks_to_create_count = random.randint(0, self.BLOCK_CREATE_MAX_COUNT)
        blocks_to_delete_count = random.randint(0, self.BLOCK_DELETE_MAX_COUNT)
        
        can_add_blocks = self._map.can_add_blocks(blocks_to_create_count)
        can_delete_blocks = self._map.can_delete_blocks(blocks_to_delete_count)
        
        if can_add_blocks and can_delete_blocks:
            random_action = random.choice((True, False))
            
            if random_action:
                self._map.scatter_random_blocks(ALLOW_CREATE_BLOCK_TYPES, self.MUTATE_BLOCK_CREATE_COUNT)
            else:
                self._map.remove_random_blocks(ALLOW_DELETE_BLOCK_TYPES, self.MUTATE_BLOCK_DELETE_COUNT)
                
        elif can_add_blocks:
            self._map.scatter_random_blocks(ALLOW_CREATE_BLOCK_TYPES, self.MUTATE_BLOCK_CREATE_COUNT)
        
        else:
            self._map.remove_random_blocks(ALLOW_DELETE_BLOCK_TYPES, self.MUTATE_BLOCK_DELETE_COUNT)

    def get_copy(self):
        return AI(
            map=self._map.get_copy(),
            input_labels=self.input_labels,
            output_labels=self.output_labels
        )
        
    def set_monitors(self, monitors):
        self._monitors = monitors