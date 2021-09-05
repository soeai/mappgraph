import os
import json
from collections import Counter

if __name__ == '__main__':

    prediction_folder = 'predictions' # folder that contain the prediction results of 16 models

    '''
    Voting the result of 16 models. For each sample, there are 16 results. 
    So, we take majority to get the final result of that sample

    '''
    apps = dict()
    for model_index in range(1, 17):
        model_folder = os.path.join(prediction_folder, 'model_%d'%model_index)
        for filename in os.listdir(model_folder):
            json_path = os.path.join(model_folder, filename)
            with open(json_path, 'r') as f:
                data = json.load(f)
                preds = data['predictions']
            if filename not in apps.keys():
                apps[filename] = [preds]
            else:
                apps[filename].append(preds)


    votings = dict()
    for k in apps.keys():
        app_name = k.split('.')[0]
        data = apps[k]
        
        models_num = len(data)
        samples_num = len(data[0])
        li = [[]]*samples_num
        for x in data:
            for i in range(samples_num):
                li[i] = li[i] + [x[i]]
        
        voting_li = [Counter(y).most_common(1)[0][0] for y in li]
        votings[k] = {'predictions': voting_li, 'labels': [app_name]*len(voting_li)}

    '''
    Save voting result into model_17 folder
    '''
    os.mkdir(os.path.join(prediction_folder, 'model_17'))   
    for k in votings.keys():
        data = votings[k]
        saved_path = os.path.join(prediction_folder, 'model_17', k)
        print(saved_path)
        with open(saved_path, 'w') as f:
            json.dump(data, f)