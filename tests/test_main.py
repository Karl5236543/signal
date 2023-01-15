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

    bot = calibrator.run()
    db.save_bot(f'best_bot', bot)
