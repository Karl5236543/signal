
INPUT_LABELS = ['a', 'b', '_c']

# ['y0', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9']
OUTPUT_LABELS = [f'y{str(i)}' for i in range(9)]

INPUT = 'input'
OUTPUT = 'output'

INPUT_SET = [
    {INPUT: {'a': 0, 'b': 0, '_c': 1}, OUTPUT: {'y0': 0, 'y1': 0, 'y2': 0, 'y3': 0, 'y4': 0, 'y5': 0, 'y6': 0, 'y7': 0, 'y8': 0,}},
    {INPUT: {'a': 0, 'b': 1, '_c': 1}, OUTPUT: {'y0': 1, 'y1': 0, 'y2': 0, 'y3': 0, 'y4': 1, 'y5': 0, 'y6': 0, 'y7': 1, 'y8': 1,}},
    {INPUT: {'a': 1, 'b': 0, '_c': 1}, OUTPUT: {'y0': 1, 'y1': 1, 'y2': 1, 'y3': 1, 'y4': 0, 'y5': 0, 'y6': 0, 'y7': 1, 'y8': 0,}},
    {INPUT: {'a': 1, 'b': 1, '_c': 1}, OUTPUT: {'y0': 1, 'y1': 0, 'y2': 1, 'y3': 0, 'y4': 0, 'y5': 0, 'y6': 0, 'y7': 1, 'y8': 1,}},
]