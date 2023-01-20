import os
from src.core.cellular_automaton.map import Map
from src.monitoring.bot_loader import BotDB
from src.monitoring.monitors import ConsoleMonitor, GUIMonitor
from src.core.individual import Individual
from src.core.calibrator import Calibrator
from src.drivers.test_driver import OneMaxDriver
import random
from src.drivers.constants import INPUT, INPUT_SET

if __name__ == '__main__':

    monitor = GUIMonitor(4)
    db = BotDB()
    ai = db.load_bot('best_bot')
    ai.set_monitors([monitor])

    data = INPUT_SET

    # random.shuffle(data)
    # while True:
    random.shuffle(data)
    for data_set in data:
        output = ai.find_result(data_set[INPUT])
        print(f'input: {data_set[INPUT]} output: {output}')

