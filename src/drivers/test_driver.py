import random


class DriverTest():

    def __init__(self):
        self.score = 0
        self.current_input = None

    data = [
        {
            'input': {'a': 0, 'b': 0}, 
            'output': {'y1': 0}
        },
        {
            'input': {'a': 0, 'b': 1}, 
            'output': {'y1': 1}
        },
        {
            'input': {'a': 1, 'b': 0}, 
            'output': {'y1': 1}
        },
        {
            'input': {'a': 1, 'b': 1}, 
            'output': {'y1': 0}
        },
    ]

    def yield_input(self):
        random.shuffle(self.data)
        for item in self.data:
            self.current_item = item
            yield item['input']

    def send_output(self, output):
        if self.current_item['output'] == output:
            self.score += 1

    def read_result(self):
        score = self.score 
        self.score = 0
        return score