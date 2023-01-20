from src.monitoring.bot_loader import BotDB
from src.monitoring.monitors import ConsoleMonitor, GUIMonitor
from src.core.individual import Individual
from src.core.calibrator import Calibrator
from src.drivers.test_driver import OneMaxDriver
from src.core.cellular_automaton.map import Map
import random


if __name__ == '__main__':

    input_labels = ['a', 'b']
    output_labels = ['y1']
    driver = OneMaxDriver()
    db = BotDB()
    monitor = GUIMonitor(1)
    ai = Individual(input_labels, output_labels)
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
    
    goal = 0
    while True:
        result = 0
        bot_copy = ai.get_copy()
        random.shuffle(data)
        for record in data:
            res = ai.find_result(record['input'])
            if res == record['output']:
                result += 1
        
        if result == 4:
            goal += 1
            
            if goal > 100:
                db.save_bot('bes_bot', bot_copy)
                break
        else:                
            bot_copy.mutate()
            goal = 0
            
        ai = bot_copy

    # best_res = None
    # for generation, results in calibrator.run():
    #     best_res = results
    #     if generation % 10 == 0:
    #         print(f'gen: {generation}\t {results}')
    
    # for bot, score in results:
    #     db.save_bot(f'best_bot_{score}', bot)

    