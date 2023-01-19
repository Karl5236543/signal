from src.monitoring.bot_loader import BotDB
from src.monitoring.monitors import ConsoleMonitor, GUIMonitor
from src.core.individual import Individual
from src.core.calibrator import Calibrator
from src.drivers.test_driver import DriverTest
from src.core.cellular_automaton.map import Map


if __name__ == '__main__':

    input_labels = ['a', 'b']
    output_labels = ['y1', 'y2', 'y3', 'y4']
    driver = DriverTest()
    goal_score = 4
    db = BotDB()

    calibrator = Calibrator(input_labels, output_labels, driver, goal_score)

    bot = calibrator.run()
    db.save_bot(f'best_bot', bot)
