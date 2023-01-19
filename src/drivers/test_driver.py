import random


class DriverTest():

    def __init__(self):
        self.score = 0
        self.current_input = None

    def yield_input(self):
        self.current_input = {str(i): random.randint(0, 1) for i in range(10)}
        yield self.current_input

    def send_output(self, output):
        if output == self.current_input:
            self.score += 1

    def read_result(self):
        score = self.score 
        self.score = 0
        return score