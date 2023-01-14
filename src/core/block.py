from src.core.constants import \
    ALLOW_TRANSFER_SIGNAL, BLOCK_STATE_ACTIVATE, BLOCK_STATE_CYCLE, BLOCK_STATE_DEACTIVATE, BLOCK_STATE_FADING, BLOCK_TYPE_INPUT, \
    BLOCK_TYPE_OUTPUT, BLOCK_TYPE_REGULATOR, BLOCK_TYPE_TRANSMITTER, IGNORE_BLOCS


class Block:
    
    def __init__(self, cords, surface, state=BLOCK_STATE_DEACTIVATE):
        self._state = state
        self._cords = cords
        self._surface = surface
        self._new_state = self._state

    def update_state(self):
        if self.allow_change_state():
            self.set_next_state()

    def allow_change_state(self):
        return \
            self.is_active() and self.allow_fading() or \
            self.is_fading() and self.allow_deactivate() or \
            self.is_deactivated() and self.allow_activate()
    
    def set_next_state(self):
        if self.is_active():
            self.repay()
            
        elif self.is_fading():
            self.deactivate()
            
        else:
            self.activate()
            
    def push_new_state(self):
        self._state = self._new_state
        
    def allow_fading(self):
        raise NotImplementedError
    
    def allow_deactivate(self):
        raise NotImplementedError
    
    def allow_activate(self):
        raise NotImplementedError
    
    def get_type(self):
        raise NotImplementedError
    
    def get_state(self):
        return self._state

    def get_around_cords(self):
        return [
            (self.get_x() + 1, self.get_y()),
            (self.get_x(), self.get_y() + 1),
            (self.get_x(), self.get_y() - 1),
            (self.get_x() - 1, self.get_y()),
        ]
        
    def activate(self):
        self._new_state = BLOCK_STATE_ACTIVATE
        
    def deactivate(self):
        self._new_state = BLOCK_STATE_DEACTIVATE

    def repay(self):
        self._new_state = BLOCK_STATE_FADING
            
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
        
    def get_copy(self):
        return self.__class__(self._cords, self._surface, self._state)
    
        
class TransmitterBlock(Block):
    
    def get_type(self):
        return BLOCK_TYPE_TRANSMITTER
    
    def allow_fading(self):
        return True
    
    def allow_deactivate(self):
        return True
    
    def allow_activate(self):
        activate = False
        around_blocks = []
        
        for block in self._surface.get_around_blocks(self):
            if block.get_type() not in IGNORE_BLOCS:
                around_blocks.append(block)
        
        for block in around_blocks:
            if block.get_type() == BLOCK_TYPE_REGULATOR and block.is_active():
                return False
            
            if block.is_active():
                activate = True
        
        return activate         
            
            
class InputBlock(TransmitterBlock):
    
    def get_type(self):
        return BLOCK_TYPE_INPUT


class OutputBlock(TransmitterBlock):
    
    def get_type(self):
        return BLOCK_TYPE_OUTPUT
    
    def allow_fading(self):
        return False
    
    
class RegulatorBlock(TransmitterBlock):
    
    def get_type(self):
        return BLOCK_TYPE_REGULATOR
    
    def allow_fading(self):
        around_blocks = []
        
        for block in self._surface.get_around_blocks(self):
            if block.get_type() not in [BLOCK_TYPE_REGULATOR]:
                around_blocks.append(block)

        return all(block.is_deactivated() for block in around_blocks)