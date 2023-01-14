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
    goal_score = 3
    db = BotDB()
    ai = AI(input_labels, output_labels)

    calibrator = Calibrator(ai, driver, goal_score)


    best_res = None
    for generation, results in calibrator.run():
        best_res = results
        if generation % 100 == 0:
            print(f'gen: {generation}\t {results}')
    
    for bot, score in results:
        db.save_bot(f'best_bot_{score}', bot)
