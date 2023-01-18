from src.monitoring.bot_loader import BotDB
from src.monitoring.monitors import ConsoleMonitor, GUIMonitor
from src.core.individual import Individual
from src.core.calibrator import Calibrator
from src.drivers.test_driver import DriverTest
from src.core.cellular_automaton.map import Map


if __name__ == '__main__':

    input_labels = ['a', 'b']
    output_labels = ['y1']
    driver = DriverTest()
    goal_score = 4
    db = BotDB()
    ai = Individual(input_labels, output_labels)
    # ai = db.load_bot('gen_53000_res_0_0_main')

    calibrator = Calibrator(ai, driver, goal_score)

    bots = calibrator.run()
    for index, bot in enumerate(bots):
        db.save_bot(f'bets_bot_{index}', bot)
    # db.save_bot(f'best_bot', bot)
