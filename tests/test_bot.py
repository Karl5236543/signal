import os
from src.core.map import Map
from src.monitoring.bot_loader import BotDB
from src.monitoring.monitors import ConsoleMonitor, GUIMonitor
from src.core.ai import AI
from src.core.calibrator import Calibrator
from src.drivers.test_driver import DriverTest

if __name__ == '__main__':
    
    # db = BotDB()
    map_template = [
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ],
        [' ', ' ', ' ', ' ', '5', ' ', ' ', ' ', ' ', ' ', ],
        [' ', ' ', ' ', ' ', '5', ' ', ' ', ' ', ' ', ' ', ],
        [' ', ' ', ' ', 'O', 'L', ' ', '5', ' ', ' ', ' ', ],
        [' ', 'I', '5', '5', '5', ' ', 'I', ' ', ' ', ' ', ],
        [' ', ' ', ' ', ' ', '5', ' ', ' ', ' ', ' ', ' ', ],
        [' ', ' ', ' ', ' ', ' ', ' ', '', ' ', ' ', ' ', ],
        [' ', ' ', ' ', ' ', '5', ' ', ' ', ' ', ' ', ' ', ],
        [' ', ' ', ' ', ' ', 'I', ' ', ' ', ' ', ' ', ' ', ],
    ]
    
    
    input_labels = ['a', 'b', 'c']
    output_labels = ['y']
    monitor = GUIMonitor(1)
    map = Map(10, 10, input_labels, output_labels)
    map.build_map_from_template(map_template)
    ai = AI(input_labels, output_labels, map=map)
    ai.set_monitors([monitor])

    input_set = (
        # {
        #     'input': {'a': 0, 'b': 0, 'c': 0},
        #     'output': {'y': 0}
        # },
        {
            'input': {'a': 1, 'b': 0, 'c': 1},
            'output': {'y': 0}
        },
        {
            'input': {'a': 1, 'b': 1, 'c': 1},
            'output': {'y': 1}
        },
        # {
        #     'input': {'a': 1, 'b': 1},
        #     'output': {'y': 0}
        # },

    )

    while True:
        for data_set in input_set:
            output = ai.find_result(data_set['input'])
        