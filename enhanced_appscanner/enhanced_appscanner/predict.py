import argparse
import json
import os
from appscanner import AppScanner


def predict(apps, model_index):
    """Predict the testing dataset by one model. The result will be save in a default folder named predictions

    Parameters
    ----------
    apps: list of apps
    model_index: determine the model used to predict

    """
    appscanner = AppScanner()

    model_path = 'appscanner_models/model_%d/model'%model_index
    prediction_folder = 'predictions/model_%d'%model_index
    if not os.path.exists(prediction_folder):
        os.mkdir(prediction_folder)

    appscanner.load_one_model(model_path)

    # predict testing samples of each class seperately
    for app in apps:
        # check existance
        json_path = os.path.join(prediction_folder, app + '.json')
        if not os.path.exists(json_path):
            appscanner.predict_one_app(app, prediction_folder)


if __name__ == "__main__":
    
    # input the number of apps before predicting (it should be matched with the number of apps when we train the models)
    parser = argparse.ArgumentParser(description='Add number of apps')
    parser.add_argument("--app_number", default='101')
    args = parser.parse_args()
    app_num = args.app_number

    # load the list of apps
    path = 'apps.json'
    with open(path, 'r') as f:
        data = json.load(f)
    apps = data[app_num]

    # Loop over 16 models. The prediction result of each model will be save in folder named predictions 
    for i in range(1, 17):
        predict(apps, i)
        print(i)
        print('--------------------------------------------------')