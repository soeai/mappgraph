import argparse
import json
from appscanner import AppScanner

if __name__ == '__main__':

    # input the number of apps before training
    parser = argparse.ArgumentParser(description='Add number of apps')
    parser.add_argument("--app_number", default='101')
    args = parser.parse_args()
    app_num = args.app_number

    # load the list of apps
    path = 'apps.json'
    with open(path, 'r') as f:
        data = json.load(f)
    apps = data[app_num]

    # train and save models
    appScannerObject = AppScanner()
    appScannerObject.fit_models(classes=apps)