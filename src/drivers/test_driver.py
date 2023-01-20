import random
from src.drivers.constants import INPUT, INPUT_SET, OUTPUT

class OneMaxDriver():

    def __init__(self):
        self.score = 0

    def yield_input(self):
        for current_set in INPUT_SET:
            self.current_set = current_set
            yield current_set[INPUT]

    def send_output(self, output):
        for key, value in self.current_set[OUTPUT].items():
            if output[key] == value:
                self.score += 1

    def read_result(self):
        score = self.score 
        self.score = 0
        return score
