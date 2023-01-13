

import random
from src.core.constants import ALL_BLOCK_TYPES, ALLOW_CREATE_BLOCK_TYPES, ALLOW_DELETE_BLOCK_TYPES, BLOCK_TYPE_INPUT, BLOCK_TYPE_OUTPUT, BLOCK_TYPE_REGULATOR, BLOCK_TYPE_TRANSMITTER
from src.core.block import InputBlock, OutputBlock, TransmitterBlock, RegulatorBlock


block_types2class_map = {
    BLOCK_TYPE_INPUT: InputBlock,
    BLOCK_TYPE_OUTPUT: OutputBlock,
    BLOCK_TYPE_TRANSMITTER: TransmitterBlock,
    BLOCK_TYPE_REGULATOR: RegulatorBlock,
}


class Map:
    
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self._field = {}
        self._block_types_map = {block_type: {} for block_type in ALL_BLOCK_TYPES}
        
        self._empty_cords = set()
        self.input_cords = {}
        self.output_cords = {}
        
    def get_block_class_by_type(self, block_type):
        return block_types2class_map[block_type]
        
    def get_blocks_count(self, allow_block_types=ALL_BLOCK_TYPES):
        return sum([len(items) for items in [self._block_types_map[block_type] for block_type in allow_block_types]])
    
    def _init_empty_cords(self):
        for y in range(self.height):
            for x in range(self.width):
                self._empty_cords.add((x, y))

    def build_map(self, field, block_types_map, empty_cords, input_cords, output_cords):
        self._field = field
        self._block_types_map = block_types_map
        
        self._empty_cords = empty_cords
        self.input_cords = input_cords
        self.output_cords = output_cords

    def build_random_map(self, input_labels, output_labels, blocks_count):
        self._init_empty_cords()

        for label in input_labels:
            cords = self.get_random_empty_cords()
            self.add_block(cords, BLOCK_TYPE_INPUT)
            self.input_cords[label] = cords

        for label in output_labels:
            cords = self.get_random_empty_cords()
            self.add_block(cords, BLOCK_TYPE_OUTPUT)
            self.output_cords[label] = cords

        for _ in range(blocks_count):
            block_type = random.choice(ALLOW_CREATE_BLOCK_TYPES)
            self.add_block(self.get_random_empty_cords(), block_type)

    def get_output(self):
        return {input_label: 1 if self.get_block(cords).is_active() else 0 \
            for (input_label, cords) in self.output_cords.items()}

    def reset_output(self):
        for _, cords in self.output_cords.items():
            block = self.get_block(cords)
            block.deactivate()
            block.push_new_state()

    def set_input(self, input):
        for input_label, cords in self.input_cords.items():
            if self.is_block_here(cords):
                block = self.get_block(cords)

                new_state = input[input_label]
                if new_state == 1:
                    block.activate()
                else:
                    block.deactivate()
                block.push_new_state()

    def get_around_blocks(self, block):
        return [self.get_block(cords) for cords in 
                self.extract_existed_cords(block.get_around_cords()) if self.is_block_here(cords)]

    def update_map_state(self):
        for _, block in self._field.items():
            block.update_state()
        
        for _, block in self._field.items():
            block.push_new_state()
        

    def extract_existed_cords(self, cords_scope):
        return [(x, y) for (x, y) in cords_scope if x < self.width and y < self.height]

    def scatter_random_blocks(self, block_types, count):
        for _ in range(count):
            rand_empty_cords = self.get_random_empty_cords()
            rand_block_type = random.choice(block_types)
            self.add_block(rand_empty_cords, rand_block_type)

    def remove_random_blocks(self, block_types, count):
        for _ in range(count):
            self.remove_block(self.get_random_no_empty_cords(allow_block_types=block_types))
            
    def can_add_blocks(self, count):
        return len(self._empty_cords) >= count
    
    def can_delete_blocks(self, count):
        return self.get_blocks_count(ALLOW_DELETE_BLOCK_TYPES) >= count
        
    def get_copy(self):
        field_copy = {}
        block_types_map = {block_type: {} for block_type in ALL_BLOCK_TYPES}
        
        for cords, block in self._field.items():
            block_copy = block.get_copy()
            field_copy[cords] = block_copy
            block_types_map[block_copy.get_type()][block_copy.get_cords()] = block_copy
             
        map_copy = Map(self.width, self.height)

        return map_copy.build_map(
            field_copy,
            block_types_map,
            self._empty_cords.copy(),
            self.input_cords.copy(),
            self.output_cords.copy()
        )
        
    def get_random_empty_cords(self):
        cords = self._empty_cords.pop()
        self._empty_cords.add(cords)
        return cords

    def get_random_no_empty_cords(self, allow_block_types):
        block_type = random.choice(
            [block_type for block_type in allow_block_types if self._block_types_map[block_type]])
        cords = random.choice(list(self._block_types_map[block_type]))
        return cords

    def add_block(self, cords, type=BLOCK_TYPE_TRANSMITTER):
        BlockClass = self.get_block_class_by_type(type)
        new_block = BlockClass(cords, self)
        self._field[cords] = new_block
        self._empty_cords.remove(cords)
        self._block_types_map[new_block.get_type()][new_block.get_cords()] = new_block
       
    def remove_block(self, cords):
        block = self.get_block(cords)
        self._field.pop(cords)
        self._empty_cords.add(cords)
        self._block_types_map[block.get_type()].pop(block.get_cords())
        
    def is_block_here(self, cords):
        return cords in self._field
    
    def get_block(self, cords):
        return self._field[cords]
    
    def get_map_state(self):
        return self._field