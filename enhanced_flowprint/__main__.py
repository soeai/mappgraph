
import json

import numpy as np

from flowprint.flowprint      import FlowPrint
from flowprint.flow_generator import FlowGenerator
from sklearn.metrics          import classification_report

import pandas as pd

DATA_PATH       = 'dataset'
TRAIN_TEST_INFO = 'train_test_info.json'


def load_data(train_test_info, _, train=True):

    X, y = list(), list()

    apps_list = [*train_test_info]
    for app in apps_list:
        app_data = pd.read_csv(f'{DATA_PATH}/{app}/{train_test_info[app][int(train)][_]}', index_col=0)
        app_data['app'] = app
        app_data = app_data[['app', 'protocol', 'stream_id', 'time', 'length', 'source_address', 'destination_address', 'source_port', 'destination_port', 'certificate']]
        app_data = app_data.where(pd.notnull(app_data), None)
        print(app_data)
        data = np.array(list(FlowGenerator().combine(app_data.values.astype('object')).values()))

        X.append(data)
        y.append(np.array([app] * data.shape[0]))

    X = list(filter(lambda x: x.shape[0] != 0, X))
    y = list(filter(lambda x: x.shape[0] != 0, y))

    try:
        X = np.concatenate(X)
        y = np.concatenate(y)
        # print(X)
    except Exception:
        X = np.array([], dtype=object)
        y = np.array([], dtype=object)

    return (X, y)


def create_flowprint(train_test_info, _):
    flowprint = FlowPrint(
        batch       = 300,
        window      = 30,
        correlation = 0.1,
        similarity  = 0.9
    )

    X, y = load_data(train_test_info, _)

    return flowprint.fit(X, y)



def __main__():

    train_test_info_file = open(f'{DATA_PATH}/{TRAIN_TEST_INFO}')
    train_test_info = json.load(train_test_info_file)
    train_test_info_file.close()

    apps_list = [*train_test_info]

    number_of_train_data = [len(train_test_info[app][0]) for app in apps_list]

    number_of_flowprints = min(number_of_train_data)

    flowprints = [create_flowprint(train_test_info, _) for _ in range(number_of_flowprints)]

    X_test, y_test = load_data(train_test_info, 0, train=False)
    fp_test = flowprints[0].fingerprinter.fit_predict(X_test)

    y_pred = flowprints[0].recognize(fp_test)

    print(classification_report(y_test, y_pred, digits=4))


if __name__ == '__main__':
    __main__()
