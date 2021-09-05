from sklearn.ensemble import RandomForestClassifier
import numpy as np
import os
import pickle
import collections
import json
from reader import Reader
from burst import Burst
from flow import Flow
from features import Features
from preprocessor import Preprocessor
import warnings
warnings.filterwarnings("ignore")

class AppScanner(object):

    def __init__(self, threshold=0.9):
        """AppScanner object for recognising applications in network traffic.
            This implementation uses a Single Large Random Forest.

            Parameters
            ----------
            threshold : float, default=0.9
                Threshold for certainty required to make a prediction.
            """
        # Set threshold
        self.threshold = threshold
        # Create classifier
        self.classifier = RandomForestClassifier(criterion='gini',
                                                 max_features='sqrt',
                                                 n_estimators=150)
        self.models = []
        
        # Initialise preprocessors
        self.reader            = Reader()
        self.preprocessor      = Preprocessor()
        self.burstifyer        = Burst()
        self.flow_extractor    = Flow()
        self.feature_extractor = Features()

    def fit(self, X, y):
        """Fit model with given training data and labels.

            Parameters
            ----------
            X : np.array of shape=(n_samples, n_features)
                Data to fit the model with.

            y : np.array of shape=(n_samples,)
                Labels corresponding to samples in X.

            Returns
            -------
            self : self
                Returns self for fit_predict method.
            """
        # Fit classifier with given data.
        self.classifier.fit(X, y)

        # Return self for fit_predict method
        return self

    """
        created by Thai-Dien Pham
    """
    def fit_models(self, models_folder='appscanner_models', classes=None):
        """Fit all models with given training data and labels.

            Parameters
            ----------
            models_folder: folder that contains dataset for training
            ___model1
            ______data
            ___model2
            ______data
            ___model3
            ______data
            ...

            Returns
            -------
            self : self
                Train all models and save them into folder named appscanner_models
            """
        for model_indx in os.listdir(models_folder):
            print('Training %s'%model_indx)

            data_path = os.path.join(models_folder, model_indx, 'data')
            model_path = os.path.join(models_folder, model_indx)
            if not os.path.exists(os.path.join(model_path, 'model')):
                apps = os.listdir(data_path) if classes is None else classes
                X, y = self.preprocessor.process_train_data(data_path, apps)
                model = RandomForestClassifier(criterion='gini',
                                                    max_features='sqrt',
                                                    n_estimators=150)
                # Fit classifier with given data.
                model.fit(X, y)
                pickle.dump(model, open(os.path.join(model_path, 'model'), 'wb'))
                self.models.append(model)
            print('..........................')

        return self

    def predict(self, X):
        """Predict the class of X from the trained model.

            Parameters
            ----------
            X : np.array of shape=(n_samples, n_features)
                Data to predict.

            Returns
            -------
            result : np.array of shape=(n_samples,)
                Prediction of labels for data X.
                Labels are -1 if they cannot be predicted.
            """
        # Get maximum prediction probabilities
        probabilities = self.classifier.predict_proba(X).max(axis=1)
        # Get prediction
        prediction = self.classifier.predict(X)

        # Set uncertain predictions to -1
        # prediction[probabilities < self.threshold] = -1

        # Return predictions
        return prediction
    
    """
        created by Thai-Dien Pham
    """
    def predict_one_sample(self, file):
        """Predict the class of a sample from the trained model.

            Parameters
            ----------
            file: path to a traffic sample (a traffic chunk of T minutes)

            Returns
            -------
            result : label of the sample
            """
        
        # Read packets
        packets = self.reader.read_csv(file)
        # Split in burts
        burst = self.burstifyer.split(packets)
        # Extract flows
        flows = self.flow_extractor.extract(burst)
        # Extract features
        features = self.feature_extractor.extract(flows)
        X = np.array(list(features.values()))
        # print('shape of X: ', X.shape)

        if X.shape[0] == 0:
            return "empty"

        prediction = self.classifier.predict(X)

        return collections.Counter(prediction).most_common(1)[0][0]
    
    """
        created by Thai-Dien Pham
    """
    def predict_test_dataset(self, path='test'):
        """Predict the class of all samples from the trained model.

            Parameters
            ----------
            path : path to test data folder
            _____app1:
            _________file1 (sample1)
            _________file2 (sample2)
            _____app2:
            _________file1 (sample1)
            _________file2 (sample2)

            Returns
            -------
            result : list of classes of all samples in the test dataset
            """
        
        paths = []
        labels = []

        for app in os.listdir(path):
            app_path = os.path.join(path, app)
            for filename in os.listdir(app_path):
                file_path = os.path.join(app_path, filename)
                paths.append(file_path)
                labels.append(app)
        
        print(paths)
        print(labels)

        predictions = []
        # labels after filtering empty duration
        new_labels = []
        for i in range(len(paths)):
            prediction = self.predict_one_sample(paths[i])
            if prediction != "empty":
                predictions.append(prediction)
                new_labels.append(labels[i]) 


        return predictions, new_labels

    """
        created by Thai-Dien Pham
    """
    def predict_one_app(self, app, prediction_folder, test_folder='test'):
        """Predict the class of all samples of one app.

            Parameters
            ----------
            path : path to traffic samples of the app
            _____app:
            _________file1 (sample1)
            _________file2 (sample2)
            ...

            Returns
            -------
            Save the result of prediction into prediction_folder
            """
        
        print(app)

        paths = []
        labels = []

        app_path = os.path.join(test_folder, app)
        for filename in os.listdir(app_path):
            file_path = os.path.join(app_path, filename)
            paths.append(file_path)
            labels.append(app)
        

        predictions = []
        # labels after filtering empty duration
        new_labels = []
        for i in range(len(paths)):
            if i > 0 and i % 20 == 0:
               print('Predicting {} th sample ...'.format(i))
            prediction = self.predict_one_sample(paths[i])
            if prediction != "empty":
                predictions.append(prediction)
                new_labels.append(labels[i]) 

        # save prediction
        saved_path = os.path.join(prediction_folder, app + '.json')
        with open(saved_path, 'w') as fp:
            json.dump({'predictions': predictions, 'labels': new_labels}, fp)

        print('Finish predicting {}'.format(app))

    def fit_predict(self, X, y):
        """Fit model and return the prediction on the same data.

            Parameters
            ----------
            X : np.array of shape=(n_samples, n_features)
                Data to fit the model with and to predict.

            y : np.array of shape=(n_samples,)
                Labels corresponding to samples in X.

            Returns
            -------
            result : np.array of shape=(n_samples,)
                Prediction of labels for data X.
                Labels are -1 if they cannot be predicted.
            """
        return self.fit(X, y).predict(X)
    
    def save_one_model(self, path):
        # save the model to disk
        # filename = 'finalized_model.sav'
        pickle.dump(self.classifier, open(path, 'wb'))
        
    def load_one_model(self, path):
        self.classifier = pickle.load(open(path, 'rb'))

    """
        created by Thai-Dien Pham
    """
    def load_models(self, path):
        for model_indx in os.listdir(path):
            print('Loading {}'.format(model_indx))
            model_path = os.path.join(path, model_indx, 'model')
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            self.models.append(model)

            print('...............DONE...............\n')

        # Return self for fit_predict method
        return self