import random
from src.drivers.constants import INPUT_SET

class OneMaxDriver():

    def __init__(self):
        self.score = 0

    def yield_input(self):
        yield from INPUT_SET

    def send_output(self, output):
        self.score += sum(output.values())

    def read_result(self):
        score = self.score 
        self.score = 0
        return score
