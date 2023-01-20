from src.monitoring.bot_loader import BotDB
from src.core.calibrator import Calibrator
from src.drivers.test_driver import OneMaxDriver
from src.monitoring.monitors import GraphMonitor
from src.drivers.constants import INPUT_LABELS, OUTPUT_LABELS

if __name__ == '__main__':

    driver = OneMaxDriver()
    goal_score = 36
    db = BotDB()

    calibrator = Calibrator(INPUT_LABELS, OUTPUT_LABELS, driver, goal_score)
    calibrator.set_monitors([GraphMonitor()])
    bot = calibrator.run()
    db.save_bot(f'best_bot', bot)
