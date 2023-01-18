from src.core.constants import BLOCK_STATE_ACTIVATE, BLOCK_STATE_DEACTIVATE, \
    BLOCK_STATE_FADING, BLOCK_TYPE_INPUT, BLOCK_TYPE_OUTPUT, BLOCK_TYPE_REGULATOR, \
    BLOCK_TYPE_TRANSMITTER, BLOCK_TYPE_TRIGGER


class Block:
    
    can_be_blocked = True

    def __init__(self, cords, surface, state=BLOCK_STATE_DEACTIVATE, new_state=None):
        self._state = state
        self._cords = cords
        self._surface = surface
        self._new_state = new_state or self._state

    def update_state(self):
        if self.allow_change_state():
            self.set_next_state()

    def allow_change_state(self):
        is_blocked = self.is_blocked()

        if self.is_active():
            around_blocks = self._surface.get_around_blocks(self, self.get_ignore_blocks_for_fading())
            return self.allow_fading(around_blocks, is_blocked)

        elif self.is_fading():
            around_blocks = self._surface.get_around_blocks(self, self.get_ignore_blocks_for_deactivate())
            return self.allow_deactivate(around_blocks, is_blocked)

        elif self.is_deactivated():
            around_blocks = self._surface.get_around_blocks(self, self.get_ignore_blocks_for_activate())
            return self.allow_activate(around_blocks, is_blocked)

    def is_blocked(self):
        return any(
            block.get_type() == BLOCK_TYPE_REGULATOR and block.is_active()
            for block in self._surface.get_around_blocks(self, ignore_blocks=[])
        )

    def get_ignore_blocks_for_fading(self):
        return self.ignore_blocks

    def get_ignore_blocks_for_deactivate(self):
        return self.ignore_blocks

    def get_ignore_blocks_for_activate(self):
        return self.ignore_blocks

    def set_next_state(self):
        if self.is_active():
            self.repay()
            
        elif self.is_fading():
            self.deactivate()
            
        else:
            self.activate()
            
    def push_new_state(self):
        if self._state == self._new_state:
            return False
        self._state = self._new_state
        return True
        
    def allow_activate(self, around_blocks, is_blocked):
        if self.can_be_blocked and is_blocked:
            return False
        return any(block.is_active() for block in around_blocks)
    
    def allow_deactivate(self, around_blocks, is_blocked):
        return True
    
    def allow_fading (self, around_blocks, is_blocked):
        return True
    
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
        
    def get_copy(self, surface):
        return self.__class__(self._cords, surface, state=self._state, new_state=self._new_state)
    
        
class TransmitterBlock(Block):
    
    ignore_blocks = [BLOCK_TYPE_OUTPUT, BLOCK_TYPE_TRIGGER]

    def get_type(self):
        return BLOCK_TYPE_TRANSMITTER


class InputBlock(TransmitterBlock):
    
    def get_type(self):
        return BLOCK_TYPE_INPUT


class OutputBlock(TransmitterBlock):
    
    def get_type(self):
        return BLOCK_TYPE_OUTPUT
    
    def allow_fading(self, around_blocks, is_blocked):
        return False
    
    
class RegulatorBlock(TransmitterBlock):
    
    ignore_blocks = [BLOCK_TYPE_REGULATOR]

    def get_type(self):
        return BLOCK_TYPE_REGULATOR
    
    def allow_fading(self, around_blocks, is_blocked):
        return all(not block.is_active() for block in around_blocks)


class TriggerBlock(Block):
    
    ignore_blocks = [BLOCK_TYPE_TRIGGER, BLOCK_TYPE_OUTPUT, BLOCK_TYPE_REGULATOR]

    def __init__(self, *args, **kwargs):
        self.can_fading = False
        super().__init__(*args, **kwargs)

    def get_type(self):
        return BLOCK_TYPE_TRIGGER
    
    def allow_fading(self, around_blocks, is_blocked):
        if self.can_fading:
            if any(block.is_active() for block in around_blocks):
                self.can_fading = False
                return True
        else:
            if all(not block.is_active() for block in around_blocks):
                self.can_fading = True
        
        return False


class TriggerBlockLocked(TriggerBlock):
    
    def __init__(self, *args, state=None, **kwargs):
        state = state or BLOCK_STATE_ACTIVATE
        super().__init__(*args, state=state, **kwargs)
        self.can_fading = True
        