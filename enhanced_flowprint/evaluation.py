
import os
import json
from sklearn.metrics         import classification_report


def __main__():

    data = []

    for app in os.listdir('prediction'):
        with open(f'prediction/{app}') as json_file:
            data.extend(json.load(json_file))
    
    data = [x for x in data if x[1] != 'unknown']
    data = list(zip(*data))
    print(classification_report(data[0], data[1], digits=4))


if __name__ == '__main__':
    __main__()

