
INPUT_LABELS = ['a', 'b']

# ['y0', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9']
OUTPUT_LABELS = [f'y{str(i)}' for i in range(10)]

INPUT_SET = [
    {'a': 0, 'b': 0, '_c': 1},
    {'a': 0, 'b': 1, '_c': 1},
    {'a': 1, 'b': 0, '_c': 1},
    {'a': 1, 'b': 1, '_c': 1},
]