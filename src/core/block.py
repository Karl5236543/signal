from core.constants import \
    BLOCK_STATE_ACTIVATE, BLOCK_STATE_DEACTIVATE, BLOCK_STATE_FADING, BLOCK_TYPE_OUTPUT, BLOCK_TYPE_TRANSMITTER


class Block:
    
    def __init__(self, cords, type, state=BLOCK_STATE_DEACTIVATE):
        self._state = state
        self._cords = cords
        self._type = type

    def get_copy(self):
        return Block(self._cords, self._type, self._state)

    def update_state(self, around_blocks):
        if self.is_transmitter():
            if self.is_fading():
                self.deactivate()

            elif self.is_active():
                self.repay()

            else:
                around_blocks = [block for block in around_blocks if block.is_transmitter()]

                for block in around_blocks:
                    if block.is_active():
                        self.activate()
                        break
        
        if self.is_output():
            around_blocks = [block for block in around_blocks if block.is_transmitter()]

            for block in around_blocks:
                if block.is_active():
                    self.activate()
                    break
    
    def is_transmitter(self):
        return self._type == BLOCK_TYPE_TRANSMITTER

    def is_output(self):
        return self._type == BLOCK_TYPE_OUTPUT

    def get_type(self):
        return self._type

    def get_around_cords(self):
        return [
            (self.get_x() + 1, self.get_y()),
            (self.get_x(), self.get_y() + 1),
            (self.get_x(), self.get_y() - 1),
            (self.get_x() - 1, self.get_y()),
        ]
        
    def activate(self):
        self._state = BLOCK_STATE_ACTIVATE
        
    def deactivate(self):
        self._state = BLOCK_STATE_DEACTIVATE

    def repay(self):
        self._state = BLOCK_STATE_FADING

    def get_state(self):
        return self._state

    def is_deactivated(self):
        return self._state == BLOCK_STATE_DEACTIVATE
    
    def is_active(self):
        return self._state == BLOCK_STATE_ACTIVATE
    
    def is_fading(self):
        return self._state == BLOCK_STATE_FADING
    
    def get_x(self):
        return self._cords[0]
    
    def get_y(self):
        return self._cords[1]

    def get_cords(self):
        return self._cords

    def set_cords(self, cords):
        self._cords = cords

    def set_x(self, x):
        self._cords[0] = x
    
    def set_y(self, y):
        self._cords[1] = y