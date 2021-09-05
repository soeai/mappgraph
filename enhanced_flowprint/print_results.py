import json
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score
import os
from statistics import stdev
import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':

    prediction_folder = 'prediction' # folder that contain the prediction results of models


    '''
    Loop over models including the voting model to print the performance
    '''
    for model_index in os.listdir(prediction_folder):
        print(model_index)
        predictions = []
        labels = []

        model_folder = os.path.join(prediction_folder, model_index)
        for filename in os.listdir(model_folder):
            path = os.path.join(model_folder, filename)
            with open(path, 'r') as fp:
                data = json.load(fp)
            predictions = predictions + data['predictions']
            labels = labels + [filename.split('.')[0]]*len(data['predictions'])

        precision = precision_score(labels, predictions, average='weighted')
        recall = recall_score(labels, predictions, average='weighted')
        f1 = f1_score(labels, predictions, average='weighted')
        acc = accuracy_score(labels, predictions)

        '''
        Print the performance of each model: precision, recall, f1, accuracy
        '''
        print('pre: ', precision)
        print('recall: ', recall)
        print('f1: ', f1)
        print('acc: ', acc)
        print('...........................................................\n')