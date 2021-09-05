

import pandas as pd
import numpy  as np
from flowprint.flow_generator import FlowGenerator



def load_csv(file, app):
    X, y = list(), list()

    app_data = pd.read_csv(file, index_col=0)
    app_data['app'] = app
    app_data = app_data[['app', 'protocol', 'stream_id', 'time', 'length', 'source_address', 'destination_address', 'source_port', 'destination_port', 'certificate']]
    app_data = app_data.where(pd.notnull(app_data), None)
    app_data = app_data.where(app_data != '', None)
    app_data = app_data[app_data.protocol != 'unknown']
    data = np.array(list(FlowGenerator().combine(app_data.values.astype('object')).values()))
    X.append(data)
    y.append(np.array([app] * data.shape[0]))

    X = list(filter(lambda x: x.shape[0] != 0, X))
    y = list(filter(lambda x: x.shape[0] != 0, y))

    return X, y