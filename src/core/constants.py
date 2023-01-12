
BLOCK_STATE_ACTIVATE = 'block_state_activate'
BLOCK_STATE_FADING = 'block_state_fading'
BLOCK_STATE_DEACTIVATE = 'block_state_deactivate'

BLOCK_TYPE_TRANSMITTER = 'block_type_transmitter'
BLOCK_TYPE_OUTPUT = 'block_type_output'
BLOCK_TYPE_INPUT = 'block_type_input'

ALL_BLOCK_TYPES = [
    BLOCK_TYPE_TRANSMITTER,
    BLOCK_TYPE_OUTPUT,
    BLOCK_TYPE_INPUT,
]

BLOCK_STATE_CYCLE = (
    BLOCK_STATE_DEACTIVATE,
    BLOCK_STATE_ACTIVATE,
    
)

ALLOW_DELETE_BLOCK_TYPES = [
    BLOCK_TYPE_INPUT,
    BLOCK_TYPE_TRANSMITTER,
]

ALLOW_TRANSFER_SIGNAL = [
    BLOCK_TYPE_INPUT,
    BLOCK_TYPE_TRANSMITTER,
] 