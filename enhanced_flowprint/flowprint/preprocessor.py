import numpy as np
import pickle
import sys

##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
from cluster import Cluster
from cross_correlation_graph import CrossCorrelationGraph
##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

try:
    from .flow_generator import FlowGenerator
    from .reader import Reader
except:
    try:
        from flow_generator import FlowGenerator
        from reader import Reader
    except Exception as e:
        raise ValueError(e)

class Preprocessor(object):
    """Preprocessor object for preprocessing flows from pcap files

        Attributes
        ----------
        reader : reader.Reader
            pcap Reader object for reading .pcap files

        flow_generator : flows.FlowGenerator
            Flow generator object for generating Flow objects
    """

    ########################################################################
    #                         Class initialisation                         #
    ########################################################################

    def __init__(self, verbose=False):
        """Preprocessor object for preprocessing flows from pcap files"""
        # Initialise Reader object
        self.reader = Reader(verbose)
        # Initialise Flow object
        self.flow_generator  = FlowGenerator()

    ########################################################################
    #                       Process files and labels                       #
    ########################################################################

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
            # On exit, exit for loop
            try:
                # print(np.array(list(self.extract(file).values())))
                data = np.array(list(self.extract(file).values()))
            except KeyboardInterrupt:
                break
            except Exception as ex:
                print("Reading {} failed: '{}'".format(file, ex), file=sys.stderr)
                continue
            # Append data to X
            X.append(data)
            # print(data.shape)
            # print(len(X))
            # Append label to y
            y.append(np.array([label] * data.shape[0]))
            # print(len(y))

        # Filter empty entries from array
        X = list(filter(lambda x: x.shape[0] != 0, X))
        y = list(filter(lambda x: x.shape[0] != 0, y))

        # Append both X and y
        try:
            X = np.concatenate(X)
            y = np.concatenate(y)
            # print(X)
        except Exception:
            X = np.array([], dtype=object)
            y = np.array([], dtype=object)

        # Return result
        return X, y

    ########################################################################
    #                         Process single file                          #
    ########################################################################

    def extract(self, infile):
        """Extract flows from given pcap file.

            Parameters
            ----------
            infile : string
                Path to input file.

            Returns
            -------
            result : dict
                Dictionary of flow_key -> flow.
            """
        # Read packets
        result = self.reader.read(infile)
        # Combine packets into flows
        result = self.flow_generator.combine(result)
        # Return result
        return result

    ########################################################################
    #                             I/O methods                              #
    ########################################################################

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

if __name__ == "__main__":
    preprocessor = Preprocessor(verbose=True)
    X, y = preprocessor.process(['test/com.carezone.caredroid.careapp.medications.pcap', 'test/com.autonavi.minimap.pcap'],
    [0, 1])
    print(X.shape)
    print(X)
    print(y)

    #### cluster #####
    cluster = Cluster()
    cluster.fit(X, y)

    cross = CrossCorrelationGraph();
    cross.fit(cluster)
    print(cross.mapping)
    print('----------------------------------------------------------------------------------------------')
    print(cross.graph)
    print('----------------------------------------------------------------------------------------------')
    print(cross.predict())





