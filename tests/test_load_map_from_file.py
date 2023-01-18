import os
from src.core.cellular_automaton.map import Map
from src.monitoring.bot_loader import BotDB
from src.monitoring.monitors import ConsoleMonitor, GUIMonitor
from src.core.individual import Individual
from src.core.calibrator import Calibrator
from src.drivers.test_driver import DriverTest
import random


if __name__ == '__main__':

    monitor = GUIMonitor(1)
    db = BotDB()
    ai = db.load_bot('bes_bot')
    ai.set_monitors([monitor])

    data = [
        {
            'input': {'a': 0, 'b': 0}, 
            'output': {'y1': 0}
        },
        {
            'input': {'a': 0, 'b': 1}, 
            'output': {'y1': 1}
        },
        {
            'input': {'a': 1, 'b': 0}, 
            'output': {'y1': 1}
        },
        {
            'input': {'a': 1, 'b': 1}, 
            'output': {'y1': 0}
        },
    ]

    # random.shuffle(data)
    # while True:
    random.shuffle(data)
    for data_set in data:
        output = ai.find_result(data_set['input'])
        print(f'input: {data_set["input"]} output: {output}')

