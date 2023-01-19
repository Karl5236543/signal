from src.monitoring.bot_loader import BotDB
from src.core.calibrator import Calibrator
from src.drivers.test_driver import DriverTest
from src.monitoring.monitors import GraphMonitor

if __name__ == '__main__':

    input_labels = [str(i) for i in range(10)]
    output_labels = [str(i) for i in range(10)]
    driver = DriverTest()
    goal_score = 4
    db = BotDB()

    calibrator = Calibrator(input_labels, output_labels, driver, goal_score)
    calibrator.set_monitors([GraphMonitor()])
    bot = calibrator.run()
    db.save_bot(f'best_bot', bot)
