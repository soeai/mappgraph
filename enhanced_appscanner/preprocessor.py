import os
import numpy as np
import pickle
from reader import Reader
from burst import Burst
from flow import Flow
from features import Features
import warnings
warnings.filterwarnings("ignore")

class Preprocessor(object):

    def __init__(self, verbose=False):
        """Preprocessor for extracting features from pcap files.

            Parameters
            ----------
            verbose : boolean, default=false
                If True, print which files are being read.
            """
        # Initialise preprocessors
        self.reader            = Reader(verbose)
        self.burstifyer        = Burst()
        self.flow_extractor    = Flow()
        self.feature_extractor = Features()

    def process(self, files, labels):
        """Extract data from files and attach given labels.

            Parameters
            ----------
            files : iterable of string
                Paths from which to extract data.

            labels : iterable of int
                Label corresponding to each path.

            Returns
            -------
            X : np.array of shape=(n_samples, n_features)
                Features extracted from files.

            y : np.array of shape=(n_samples,)
                Labels for each flow extracted from files.
            """
        # Initialise X and y
        X, y = list(), list()

        # Loop over all given files
        for file, label in zip(files, labels):
            data = np.array(list(self.extract(file).values()))
            # Append data to X
            X.append(data)
            # Append label to y
            y.append(np.array([label] * data.shape[0]))

        # Filter empty entries from array
        X = list(filter(lambda x: x.shape[0] != 0, X))
        y = list(filter(lambda x: x.shape[0] != 0, y))

        # Append both X and y
        X = np.concatenate(X)
        y = np.concatenate(y)

        # Return result
        return X, y

    """
        created by Thai-Dien Pham
    """
    def process_train_data(self, data_path, classes):
        """Extract data from files and attach given labels.

            Parameters
            ----------
            folder: folder that contains all data for training one model
            classes: list of apps used to train the model (maximum is 101 apps)

            Returns
            -------
            X : np.array of shape=(n_samples, n_features)
                Features extracted from files.

            y : np.array of shape=(n_samples,)
                Labels for each flow extracted from files.
            """

        files = []
        labels = []
        filenames = os.listdir(data_path)
        filenames = [filename for filename in filenames if "_".join(filename.split('_')[:-2]) in classes]
        for filename in filenames:
            files.append(os.path.join(data_path, filename))
            labels.append("_".join(filename.split('_')[:-2]))
        
        # Initialise X and y
        X, y = list(), list()

        # Loop over all given files
        for file, label in zip(files, labels):
            data = np.array(list(self.extract(file).values()))
            # Append data to X
            X.append(data)
            # Append label to y
            y.append(np.array([label] * data.shape[0]))

        # Filter empty entries from array
        X = list(filter(lambda x: x.shape[0] != 0, X))
        y = list(filter(lambda x: x.shape[0] != 0, y))

        # Append both X and y
        X = np.concatenate(X)
        y = np.concatenate(y)

        # Return result
        return X, y

    def extract(self, file):
        """Extract flow features from given pcap file.

            Parameters
            ----------
            file : string
                Path to pcap file from which to extract flow features.

            Returns
            -------
            result : dict
                Dictionary of flow_key -> np.array of flow_features
                Flow tuple is defined as (timestamp, src, sport, dst, dport)
            """
        # Read packets
        # result = self.reader.read(file)
        result = self.reader.read_csv(file)
        # Split in burts
        result = self.burstifyer.split(result)
        # Extract flows
        result = self.flow_extractor.extract(result)
        # Extract features
        result = self.feature_extractor.extract(result)

        # Return result
        return result

    def save(self, outfile, X, y):
        """Save data to given outfile.

            Parameters
            ----------
            outfile : string
                Path of file to save data to.

            X : np.array of shape=(n_samples, n_features)
                Features extracted from files.

            y : np.array of shape=(n_samples,)
                Labels for each flow extracted from files.
            """
        with open(outfile, 'wb') as outfile:
            pickle.dump((X, y), outfile)

    def load(self, infile):
        """Load data from given infile.

            Parameters
            ----------
            infile : string
                Path of file from which to load data.

            Returns
            -------
            X : np.array of shape=(n_samples, n_features)
                Features extracted from files.

            y : np.array of shape=(n_samples,)
                Labels for each flow extracted from files.
            """
        with open(infile, 'rb') as infile:
            return pickle.load(infile)