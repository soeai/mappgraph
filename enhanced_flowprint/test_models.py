import warnings
warnings.filterwarnings("ignore")

import os
import json
from load_csv import load_csv
from flowprint.flowprint     import FlowPrint
import numpy as np
import operator

import signal
from multiprocessing import Pool
from multiprocessing import current_process
from multiprocessing import cpu_count


MODEL_PATH = 'models'
TEST_DATA_PATH = 'test_data'
RESULT_FOLDER = 'prediction'
NUMBER_OF_PROCESSED = cpu_count() // 2


def get_max_frequent(x):

    if len(x) == 0:
        return 'unknown_unknown'

    frequencies = {}
    for item in x:
        if item in frequencies:
            frequencies[item] += 1
        else:
            frequencies[item] = 1

    return max(frequencies.items(), key=operator.itemgetter(1))[0]


def predict(model_on_memory_file, app_sample):
    
    X, y = app_sample

    model = FlowPrint()
    model.load_on_memory_file(model_on_memory_file)
    fp_test = model.fingerprinter.fit_predict(X)
    y_pred = [list(_)[0] for _ in model.recognize(fp_test)]
    prediction = '_'.join(get_max_frequent(y_pred).split('_')[:-2])

    return prediction


def test_model_with_app(model, app_samples):
    predictions = []

    for app_sample in app_samples:
        prediction = predict(model, app_sample)
        predictions.append(prediction)

    return predictions

class KeyboardInterruptError(Exception): pass

def test_model(app_name):

    try:
        app_samples_ = os.listdir(f'{TEST_DATA_PATH}/{app_name}')
        app_samples = []

        for app_sample_ in app_samples_:
            X, y = list(), list()

            app_path = f'{TEST_DATA_PATH}/{"_".join(app_sample_.split("_")[:-2])}/{app_sample_}'
            X_, y_ = load_csv(app_path, 'y')
            try:
                X = np.concatenate(X_)
                y = np.concatenate(y_)
            except Exception:
                X = np.array([], dtype=object)
                y = np.array([], dtype=object)
            
            app_samples.append((X, y))
        models_list = [_.split('.')[0] for _ in os.listdir(MODEL_PATH)]
        for model_name in models_list:
            if not os.path.exists(f'{RESULT_FOLDER}/{model_name}'):
                os.makedirs(f'{RESULT_FOLDER}/{model_name}')

            with open(f'{MODEL_PATH}/{model_name}.model', 'r') as model_file:
                model = json.load(model_file)

            result_file = f'{RESULT_FOLDER}/{model_name}/{app_name}.json'
            if os.path.isfile(result_file):
                print(f'[PROCESS {current_process().name}] < PASSED >: Model {model_name}\t{app_name}\talready predicted')
                continue

            predictions = test_model_with_app(model, app_samples)
            
            with open(result_file, 'w') as file:
                json.dump(
                    {
                        'predictions': predictions,
                    },
                    file,
                )
            
            print(f'[PROCESS {current_process().name}] < DONE >: Model {model_name}\t{app_name}')
    
    except KeyboardInterrupt:
        raise KeyboardInterruptError()


if __name__ == '__main__':

    apps_list = list(map(lambda x: x.split('.')[0], os.listdir(TEST_DATA_PATH)))

    with Pool(NUMBER_OF_PROCESSED) as pool:
        print(f'NUMBER OF PROCESS {pool._processes}')

        try:
            pool.map(test_model, apps_list)
        except KeyboardInterrupt:
            print('Caught KeyboardInterrupt, terminating workers')
            pool.terminate()
            pool.join()

    print('done')
