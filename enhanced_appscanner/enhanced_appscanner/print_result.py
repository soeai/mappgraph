import json
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score
import os
from statistics import stdev
import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':

    prediction_folder = 'predictions' # folder that contain the prediction results of 16 models

    precision_li = []
    recall_li = []
    f1_li = []
    acc_li = []

    '''
    Loop over 17 models including the voting model to print the performance
    '''
    for model_index in range(1, 18):
        print('Model_%d'%model_index if model_index < 17 else 'Voting model')
        predictions = []
        labels = []

        model_folder = os.path.join(prediction_folder, 'model_%d'%model_index)
        for filename in os.listdir(model_folder):
            path = os.path.join(model_folder, filename)
            with open(path, 'r') as fp:
                data = json.load(fp)
            predictions = predictions + data['predictions']
            labels = labels + data['labels']

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

        # save the performance of each model (not including the voting model) to do some statistic later
        if model_index < 17:
            precision_li.append(precision)
            recall_li.append(recall)
            f1_li.append(f1)
            acc_li.append(acc)
        


    '''
    Print mean and standard deviation of the precision, recall, f1, accuracy of 16 models (not including the voting model)
    '''

    # mean
    print('precision mean: ', sum(precision_li)/16)
    print('recall mean: ', sum(recall_li)/16)
    print('f1 mean: ', sum(f1_li)/16)
    print('acc mean: ', sum(acc_li)/16)

    print('...........................................................\n')

    # std
    print('precision std: ', stdev(precision_li))
    print('recall std: ', stdev(recall_li))
    print('f1 std: ', stdev(f1_li))
    print('acc std: ', stdev(acc_li))