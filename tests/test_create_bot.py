import os
import random
from src.core.cellular_automaton.map import Map
from src.monitoring.bot_loader import BotDB
from src.monitoring.monitors import ConsoleMonitor, GUIMonitor
from src.core.individual import Individual
from src.core.calibrator import Calibrator
from src.drivers.test_driver import DriverTest

if __name__ == '__main__':
    
    # db = BotDB()
    # map_template = [
    #     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ],
    #     [' ', ' ', ' ', ' ', ' ', ' ', '5', ' ', ' ', ' ', ],
    #     [' ', ' ', ' ', ' ', 'T', 'L', '5', ' ', ' ', ' ', ],
    #     [' ', ' ', ' ', ' ', 'T', 'L', '5', ' ', ' ', ' ', ],
    #     [' ', ' ', ' ', ' ', '5', ' ', '5', ' ', ' ', ' ', ],
    #     [' ', ' ', ' ', ' ', '5', ' ', '5', ' ', ' ', ' ', ],
    #     [' ', ' ', ' ', ' ', '5', ' ', '5', ' ', ' ', ' ', ],
    #     [' ', ' ', ' ', ' ', 'I', '5', '5', ' ', ' ', ' ', ],
    #     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ],
    #     [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ],
    # ]
    
    
    input_labels = ['a', 'b', '_c']
    output_labels = ['y']
    # monitor = GUIMonitor(1)
    db = BotDB()
    ai = Individual(input_labels, output_labels)
    # ai.set_monitors([monitor])

    input_set = [
        {
            'input': {'a': 0, 'b': 0, '_c': 1},
            'output': {'y': 0}
        },
        {
            'input': {'a': 0, 'b': 1, '_c': 1},
            'output': {'y': 1}
        },
        {
            'input': {'a': 1, 'b': 0, '_c': 1},
            'output': {'y': 1}
        },
        {
            'input': {'a': 1, 'b': 1, '_c': 1},
            'output': {'y': 0}
        },

    ]

    goal_res = 0
    gen = 0
    while True:
        res = 0
        gen += 1
        bot_copy = ai.get_copy()
        random.shuffle(input_set)
        for data_set in input_set:
            output = ai.find_result(data_set['input'])
            if output == data_set['output']:
                res += 1

        if gen % 100 == 0:
            print(f'gen: {gen}\r')
        
        if res == 4:
            goal_res += 1
            if goal_res == 50:
                db.save_bot('best_bot', bot_copy)
                break
        else:
            goal_res = 0    
            bot_copy.mutate()
        
        ai = bot_copy