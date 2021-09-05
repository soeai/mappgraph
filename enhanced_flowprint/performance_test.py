import warnings
warnings.filterwarnings("ignore")

import os
import sys
import json
from load_csv import load_csv
from flowprint.flowprint     import FlowPrint
import numpy as np
import operator

import signal
from multiprocessing import Pool
from multiprocessing import current_process
from multiprocessing import cpu_count
from multiprocessing import Manager


from random import choice
from time import time
check_points = []


from test_models import predict


MODEL_PATH = 'C:/Users/hothi/Desktop/Dien/models/100_models_T5_t10'
TEST_APP = 'C:/Users/hothi/Desktop/Dien/test_data/T5/among_us'
RESULT_FOLDER = 'C:/Users/hothi/Desktop/Dien/performance_test/models_T5_t10'


def load_model(model_name):
    with open(f'{MODEL_PATH}/{model_name}', 'r') as model_file:
        return json.load(model_file)



def load_sample():
    samples_list = os.listdir(TEST_APP)
    random_selected_sample = choice(samples_list)

    sample_path = f'{TEST_APP}/{random_selected_sample}'

    X_, y_ = load_csv(sample_path, 'y')
    try:
        X = np.concatenate(X_)
        y = np.concatenate(y_)
    except Exception:
        X = np.array([], dtype=object)
        y = np.array([], dtype=object)
    
    return (X, y)



class KeyboardInterruptError(Exception): pass

def run_test(x):
    try:
        model, sample, check_points = x
        predict_app = predict(model, sample)
        check_point = time()
        print(f'[{predict_app}]: {check_point}')
        check_points.append(check_point)
    except KeyboardInterrupt:
        raise KeyboardInterruptError()




def run_test_factory(sample):
    return lambda model: run_test(model, sample)



def save_result(result):
    save_file_path = f'{RESULT_FOLDER}/{TEST_APP.split("/")[-1]}.json'
    with open(save_file_path, 'w') as file:
        json.dump(result, file, indent=4)



if __name__ == '__main__':

    sample = load_sample()

    models_list = [load_model(_) for _ in os.listdir(MODEL_PATH)]

    result = {}

    for number_of_process in range(1, 13):

        print()
        print(f'Start Performing testing with {number_of_process} process')
        print()

        with Manager() as manager:
            check_points = manager.list()
            
            with Pool(number_of_process) as pool:
                try:
                    pool.map(run_test, [(model, sample, check_points) for model in models_list])
                except KeyboardInterrupt:
                    print('Caught KeyboardInterrupt, terminating workers')
                    pool.terminate()
                    pool.join()

                    print('TERMINATED')
                    sys.exit()
            
            result[str(number_of_process)] = [_ - check_points[0] for _ in check_points]
    

    save_result(result)

    print()
    print('DONE')
    print()


