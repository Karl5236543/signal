from src.monitoring.bot_loader import BotDB
from src.monitoring.monitors import ConsoleMonitor, GUIMonitor
from src.core.ai import AI
from src.core.calibrator import Calibrator
from src.drivers.test_driver import DriverTest

if __name__ == '__main__':
    
    input_labels = ('a', 'b')
    output_labels = ('y', )
    goal_score = 4
    driver = DriverTest()
    db = BotDB()
    ai = AI(input_labels, output_labels)
    ai = db.load_bot('best_bot')
    calibrator = Calibrator(
        seed=ai,
        driver=driver,
        goal_score=goal_score
    )

    best_results = None
    for generation, results in calibrator.run():
        best_results = results
        if generation % 100 == 0:
            print(f'gen: {generation} ({best_results})')
            for bot, score in best_results:
                db.save_bot(f'test_bot_gen_{generation}_score_{score}', bot)