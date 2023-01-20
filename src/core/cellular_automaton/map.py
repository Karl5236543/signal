

import random
import uuid
from src.core.constants import ALL_BLOCK_TYPES, ALLOW_CREATE_BLOCK_TYPES, ALLOW_DELETE_BLOCK_TYPES, \
    BLOCK_TYPE_INPUT, BLOCK_TYPE_OUTPUT, BLOCK_TYPE_REGULATOR, BLOCK_TYPE_TRANSMITTER, BLOCK_TYPE_TRIGGER, \
    BLOCK_TYPE_TRIGGER_LOCKED
from src.core.cellular_automaton.block import \
    InputBlock, OutputBlock, TransmitterBlock, RegulatorBlock, TriggerBlock, TriggerBlockLocked


block_types2class_map = {
    BLOCK_TYPE_INPUT: InputBlock,
    BLOCK_TYPE_OUTPUT: OutputBlock,
    BLOCK_TYPE_TRANSMITTER: TransmitterBlock,
    BLOCK_TYPE_REGULATOR: RegulatorBlock,
    BLOCK_TYPE_TRIGGER: TriggerBlock,
    BLOCK_TYPE_TRIGGER_LOCKED: TriggerBlockLocked
}

block_symbol2type_map = {
    'I': BLOCK_TYPE_INPUT,
    'O': BLOCK_TYPE_OUTPUT,
    '5': BLOCK_TYPE_TRANSMITTER,
    'L': BLOCK_TYPE_REGULATOR,
    't': BLOCK_TYPE_TRIGGER_LOCKED,
    'T': BLOCK_TYPE_TRIGGER,
}


class Map:

    def __init__(self, width, height, input_labels, output_labels, main_output_label):
        self.width = width
        self.height = height
        self.main_output_label = main_output_label
        self.id = uuid.uuid4()

        self._field = {}
        self._block_types_map = {block_type: {} for block_type in ALL_BLOCK_TYPES}
        
        self._empty_cords = set()
        self.input_cords = {}
        self.output_cords = {}
        self.input_labels = input_labels
        self.output_labels = output_labels
        
    def __get_block_class_by_type(self, block_type):
        return block_types2class_map[block_type]
        
    def get_blocks_count(self, allow_block_types=ALL_BLOCK_TYPES):
        return sum([len(items) for items in [self._block_types_map[block_type] for block_type in allow_block_types]])
    
    def __repr__(self) -> str:
        return f'<Map {self.id}>'
    
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
        
    def build_map_from_template(self, template):
        self._init_empty_cords()
        
        for index_row, row in enumerate(template):
            for index_col, col in enumerate(row):
                
                cords = (index_col, index_row)
                block_type = block_symbol2type_map.get(col, None)
                
                if block_type:
                    if block_type == BLOCK_TYPE_INPUT:
                        self.__add_input(cords, self.input_labels.pop())
                    elif block_type == BLOCK_TYPE_OUTPUT:
                        self.__add_output(cords, self.output_labels.pop())
                    else:
                        self.__add_block(cords, block_type)
        
        self.update_map_state()
                        
    def build_random_map(self, blocks_count):
        self._init_empty_cords()

        for label in self.input_labels:
            cords = self.__get_random_empty_cords()
            self.__add_input(cords, label)

        for label in self.output_labels:
            cords = self.__get_random_empty_cords()
            self.__add_output(cords, label)

        for _ in range(blocks_count):
            block_type = random.choice(ALLOW_CREATE_BLOCK_TYPES)
            self.__add_block(self.__get_random_empty_cords(), block_type)
        
        self.update_map_state()

    def get_main_output(self):
        cords = self.output_cords[self.main_output_label]
        return 1 if self.__get_block(cords).is_active() else 0

    def get_output(self):
        return {output_label: 1 if self.__get_block(cords).is_active() else 0 \
            for (output_label, cords) in self.output_cords.items()}

    def reset_output(self):
        for _, cords in self.output_cords.items():
            block = self.__get_block(cords)
            block.deactivate()
            block.push_new_state()

    def set_input(self, input):
        for input_label, cords in self.input_cords.items():
            if self.__is_block_exist(cords):
                block = self.__get_block(cords)

                new_state = input[input_label]
                if new_state == 1:
                    block.activate()
                else:
                    block.deactivate()
                block.push_new_state()

    def get_around_blocks(self, block, ignore_blocks):
        arownd_blocks = [
            self.__get_block(cords) for cords in 
            self.extract_existed_cords(block.get_around_cords())
            if self.__is_block_exist(cords)
        ]

        return [block for block in arownd_blocks if block.get_type() not in ignore_blocks]

    def update_map_state(self):
        for _, block in self._field.items():
            block.update_state()
        
        block_update_count = 0
        for _, block in self._field.items():
            updated = block.push_new_state()
            if updated:
                block_update_count += 1
        
        return block_update_count

    def extract_existed_cords(self, cords_scope):
        return [(x, y) for (x, y) in cords_scope if x < self.width and y < self.height]

    def scatter_random_blocks(self, block_types, count):
        for _ in range(count):
            rand_empty_cords = self.__get_random_empty_cords()
            rand_block_type = random.choice(block_types)
            self.__add_block(rand_empty_cords, rand_block_type)

    def remove_random_blocks(self, block_types, count):
        for _ in range(count):
            self.__remove_block(self.__get_random_no_empty_cords(allow_block_types=block_types))
            
    def can_add_blocks(self, count):
        return len(self._empty_cords) >= count
    
    def can_delete_blocks(self, count):
        return self.get_blocks_count(ALLOW_DELETE_BLOCK_TYPES) >= count
        
    def get_copy(self):
        field_copy = {}
        block_types_map = {block_type: {} for block_type in ALL_BLOCK_TYPES}
        
        map_copy = Map(self.width, self.height, self.input_labels, self.output_labels, self.main_output_label)
        
        for cords, block in self._field.items():
            block_copy = block.get_copy(surface=map_copy)
            field_copy[cords] = block_copy
            block_types_map[block_copy.get_type()][block_copy.get_cords()] = block_copy
             

        map_copy.build_map(
            field_copy,
            block_types_map,
            self._empty_cords.copy(),
            self.input_cords.copy(),
            self.output_cords.copy()
        )

        return map_copy
        
    def __get_random_empty_cords(self):
        empty_cords = list(self._empty_cords)
        cords = random.choice(empty_cords)
        return cords

    def __get_random_no_empty_cords(self, allow_block_types):
        block_type = random.choice(
            [block_type for block_type in allow_block_types if self._block_types_map[block_type]])
        cords = random.choice(list(self._block_types_map[block_type]))
        return cords

    def __add_input(self, cords, label):
        self.__add_block(cords, BLOCK_TYPE_INPUT)
        self.input_cords[label] = cords
        
    def __add_output(self, cords, label):
        self.__add_block(cords, BLOCK_TYPE_OUTPUT)
        self.output_cords[label] = cords

    def __add_block(self, cords, type=BLOCK_TYPE_TRANSMITTER):
        BlockClass = self.__get_block_class_by_type(type)
        new_block = BlockClass(cords, self)
        self._field[cords] = new_block
        self._empty_cords.remove(cords)
        self._block_types_map[new_block.get_type()][new_block.get_cords()] = new_block
       
    def __remove_block(self, cords):
        block = self.__get_block(cords)
        self._field.pop(cords)
        self._empty_cords.add(cords)
        self._block_types_map[block.get_type()].pop(block.get_cords())
        
    def __is_block_exist(self, cords):
        return cords in self._field
    
    def __get_block(self, cords):
        return self._field[cords]
    
    def get_map_state(self):
        return self._field