import os
from src.core.map import Map
from src.monitoring.bot_loader import BotDB
from src.monitoring.monitors import ConsoleMonitor, GUIMonitor
from src.core.ai import AI
from src.core.calibrator import Calibrator
from src.drivers.test_driver import DriverTest

if __name__ == '__main__':

    monitor = GUIMonitor(1)
    db = BotDB()
    ai = db.load_bot('best_bot')
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

    for data_set in input_set:
        output = ai.find_result(data_set['input'])
        print(f'intupt: {data_set["input"]} output: {output}')


