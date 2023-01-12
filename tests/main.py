from src.core.ai import AI
from src.core.calibrator import Calibrator
from src.drivers.test_driver import DriverTest

if __name__ == '__main__':
    
    input_labels = ('a', 'b')
    output_labels = ('y', )
    
    ai = AI(input_labels, output_labels)
    # driver = DriverTest

    ai.find_result(input={'a': 1, 'b': 2})


    # calibrator = Calibrator(ai, driver)

    # for result in calibrator.run():
    #     print(result)