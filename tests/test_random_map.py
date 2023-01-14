from src.monitoring.bot_loader import BotDB
from src.monitoring.monitors import ConsoleMonitor, GUIMonitor
from src.core.ai import AI
from src.core.calibrator import Calibrator
from src.drivers.test_driver import DriverTest
from src.core.map import Map


if __name__ == '__main__':

    input_labels = ['a', 'b']
    output_labels = ['y']
    driver = DriverTest()
    monitor = GUIMonitor(1)
    ai = AI(input_labels, output_labels)
    ai.set_monitors([monitor])

    while True:
        bot_copy = ai.get_copy()
        ai.find_result({'a': 1, 'b': 0})
        bot_copy.mutate()
        ai = bot_copy

    # best_res = None
    # for generation, results in calibrator.run():
    #     best_res = results
    #     if generation % 10 == 0:
    #         print(f'gen: {generation}\t {results}')
    
    # for bot, score in results:
    #     db.save_bot(f'best_bot_{score}', bot)

    