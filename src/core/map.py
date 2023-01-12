

import random
from src.core.block import Block
from src.core.constants import ALL_BLOCK_TYPES, BLOCK_TYPE_INPUT, BLOCK_TYPE_OUTPUT, BLOCK_TYPE_TRANSMITTER


block_types_map = [
    BLOCK_TYPE_INPUT: InputBlock
]


class Map:
    
    def __init__(self, width, height, field=None, empty_cords=None, input_cords=None, output_cords=None):
        self._field = field or {}
        self._empty_cords = empty_cords or set()
        self.width = width
        self.height = height
        self.input_cords = input_cords or {}
        self.output_cords = output_cords or {}
        
    def get_blocks_count(self):
        return len(self._field) - (len(self.input_cords) + len(self.output_cords))

    def _init_empty_cords(self):
        for y in range(self.height):
            for x in range(self.width):
                self._empty_cords.add((x, y))

    def build_random_map(self, input_labels, output_labels, blocks_count):
        self._init_empty_cords()

        for label in input_labels:
            cords = self.get_rand_empty_cords(type=BLOCK_TYPE_INPUT)
            self.add_block(cords)
            self.input_cords[label] = cords

        for label in output_labels:
            cords = self.get_rand_empty_cords()
            self.add_block(cords, type=BLOCK_TYPE_OUTPUT)
            self.output_cords[label] = cords

        for _ in range(blocks_count):
            self.add_block(self.get_rand_empty_cords())

    def get_output(self):
        return {input_label: 1 if self.get_block(cords).is_active() else 0 \
            for (input_label, cords) in self.output_cords.items()}

    def reset_output(self):
        for _, cords in self.output_cords.items():
            block = self.get_block(cords)
            block.deactivate()

    def set_input(self, input):
        for input_label, cords in self.input_cords.items():
            if self.is_block_here(cords):
                block = self.get_block(cords)

                new_state = input[input_label]
                if new_state == 1:
                    block.activate()
                else:
                    block.deactivate() 

    def get_around_blocks(self, block, allow_block_types=ALL_BLOCK_TYPES):
        return [self.get_block(cords) for cords in block.get_around_cords() if self.is_block_here(cords)]

    def update_map_state(self):
        for _, block in self._field.items():
            around_block = [self.get_block(cords) for cords in block.get_around_cords() if self.is_block_here(cords)]
            block.update_state(around_block)

    def extract_existed_cords(self, cords_scope):
        return [(x, y) for (x, y) in cords_scope if x < self.width and y < self.height]

    def scatter_blocks(self, block_type, count):
        for _ in range(count):
            rand_empty_cords = self.get_rand_empty_cords() 
            self._field[rand_empty_cords] = Block(rand_empty_cords, block_type)

    def remove_rand_blocks(self, block_type, count):
        for _ in range(count):
            self.remove_block(self.get_random_no_empty_cords(allow_block_types=[block_type])) 

    def get_copy(self):
        field_copy = {cords: block.get_copy() for (cords, block) in self._field.items()}
        return Map(
            self.width,
            self.height,
            field_copy,
            self._empty_cords.copy(),
            self.input_cords.copy(),
            self.output_cords.copy()
        )

    def get_rand_empty_cords(self):
        cords = self._empty_cords.pop()
        self._empty_cords.add(cords)
        return cords

    def get_random_no_empty_cords(self, allow_block_types):
        while True:
            cords = random.choice(list(self._field.keys()))
            if self._field[cords].get_type() in allow_block_types:
                return cords

    def add_block(self, cords, type=BLOCK_TYPE_TRANSMITTER):
       self._field[cords] = Block(cords, type)
       self._empty_cords.remove(cords)
       
    def remove_block(self, cords):
        self._field.pop(cords)
        self._empty_cords.add(cords)
        
    def is_block_here(self, cords):
        return cords in self._field
    
    def get_block(self, cords):
        return self._field[cords]
    
    def get_map_state(self):
        yield from self._field