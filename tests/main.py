from src.monitoring.monitors import ConsoleMonitor, GUIMonitor
from src.core.ai import AI
from src.core.calibrator import Calibrator
from src.drivers.test_driver import DriverTest

if __name__ == '__main__':
    
    input_labels = ('a', 'b')
    output_labels = ('y', )
    
    ai = AI(input_labels, output_labels)
    ai.set_monitors([ConsoleMonitor(), GUIMonitor()])
    # driver = DriverTest

    input_set = (
        {'a': 0, 'b': 0},
        {'a': 0, 'b': 1},
        {'a': 1, 'b': 0},
        {'a': 1, 'b': 1},
    )

    for input_data in input_set:
        output = ai.find_result(input_data)


    # calibrator = Calibrator(ai, driver)

    # for result in calibrator.run():
    #     print(result)