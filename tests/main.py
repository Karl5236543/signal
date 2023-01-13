from src.monitoring.monitors import ConsoleMonitor, GUIMonitor
from src.core.ai import AI
from src.core.calibrator import Calibrator
from src.drivers.test_driver import DriverTest

if __name__ == '__main__':
    
    input_labels = ('a', 'b')
    output_labels = ('y', )
    
    monitor = GUIMonitor(1)
    ai = AI(input_labels, output_labels)
    ai.set_monitors([monitor])
    # driver = DriverTest

    input_set = (
        {'a': 1, 'b': 1},
        # {'a': 1, 'b': 0},
        # {'a': 1, 'b': 1},
        # {'a': 0, 'b': 0},
    )

    for _ in range(1000):
        for input_data in input_set:
            output = ai.find_result(input_data)
        ai.mutate()


    # calibrator = Calibrator(ai, driver)

    # for result in calibrator.run():
    #     print(result)