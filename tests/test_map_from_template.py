import os
import random
from src.core.map import Map
from src.monitoring.bot_loader import BotDB
from src.monitoring.monitors import ConsoleMonitor, GUIMonitor
from src.core.ai import AI
from src.core.calibrator import Calibrator
from src.drivers.test_driver import DriverTest

if __name__ == '__main__':
    
    map_template = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ],
        [' ', ' ', ' ', ' ', ' ', 'I', '5', '5', '5', 'O', ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'L', ' ', ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'I', 't', ' ', ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '5', '5', ' ', ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ],
    ]
    
    
    input_labels = ['a', 'b']
    output_labels = ['y']
    
    map = Map(10, 10, input_labels, output_labels)
    map.build_map_from_template(map_template)
    
    ai = AI(surface=map)
    monitor = GUIMonitor(1)
    ai.set_monitors([monitor])

    input_set = [
        {
            'input': {'a': 0, 'b': 0},
            'output': {'y': 0}
        },
        {
            'input': {'a': 0, 'b': 1},
            'output': {'y': 1}
        },
        {
            'input': {'a': 1, 'b': 0},
            'output': {'y': 1}
        },
        {
            'input': {'a': 1, 'b': 1},
            'output': {'y': 0}
        },

    ]

    # while True:
    for input in input_set:
        res = ai.find_result(input['input'])
        print(f'in: {input["input"]}\tout: {res}')