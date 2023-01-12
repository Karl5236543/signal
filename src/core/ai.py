import random
from core.constants import BLOCK_TYPE_TRANSMITTER
from core.map import Map

class AI:

    MAP_WIDTH = 50
    MAP_HEIGHT = 50
    BLOCKS_COUNT = 300
    MAP_UPDATE_ITERATION_COUNT = 250
    MUTATE_BLOCK_CREATE_COUNT = 5
    MUTATE_BLOCK_DELETE_COUNT = 5

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

    # TODO:
    def mutate(self):
        if self._map.get_blocks_count() < self.MUTATE_BLOCK_DELETE_COUNT or random.choice((True, False)):
            self._map.scatter_blocks(BLOCK_TYPE_TRANSMITTER, self.MUTATE_BLOCK_CREATE_COUNT)
        else:
            self._map.remove_rand_blocks(BLOCK_TYPE_TRANSMITTER, self.MUTATE_BLOCK_DELETE_COUNT)

    def get_copy(self):
        return AI(
            map=self._map.get_copy(),
            input_labels=self.input_labels,
            output_labels=self.output_labels
        )
        
    def set_monitors(self, monitors):
        self._monitors = monitors