import numpy as np
import pandas as pd

class Features(object):

    def extract(self, flows):
        """Extract the features for each flow in flows.
            Features are computed for incoming packets, outgoing packets and a
            combination of incoming and outgoing packets. For the features per
            flow type, see self.features.

            Parameters
            ----------
            flows : dict
                Dictionary of flow_key -> packet lengths.
                Flow tuple is defined as (timestamp, src, sport, dst, dport)
                Packet lengths are positive for outgoing messages
                and negative if incoming messages.

            Returns
            -------
            result : dict
                Dictionary of flow_key -> flow features.
                See extract_single for flow features.
            """
        # Initialise result
        result = dict()

        # Loop over all flows
        for flow_id, flow in flows.items():
            # Extract features per flow
            result[flow_id] = self.extract_single(flow)

        # Return result
        return result

    def extract_single(self, flow):
        """Extract the features for each flow.
            Features are computed for incoming packets, outgoing packets and a
            combination of incoming and outgoing packets. For the features per
            flow type, see self.features.

            Parameters
            ----------
            flow : np.array of shape=(n_samples,)
                Length of packets in flows.

            Returns
            -------
            result : np.array of shape=(54,)
                All features of given flow.
            """
        # Get three series of flows
        incoming = np.array([f for f in flow if f <  0])
        outgoing = np.array([f for f in flow if f >= 0])
        combined = flow

        # Get result for given arrays
        result = np.array(
            self.features(incoming) +
            self.features(outgoing) +
            self.features(combined)
        )

        # Set nan values to 0
        result[np.isnan(result)] = 0

        # Return result
        return result

    def features(self, array):
        """For each array compute the following features.
            - Minimum
            - Maximum
            - Mean
            - Median absolute deviation
            - Standard deviation
            - Variance
            - Skew
            - Kurtosis
            - Percentiles (from 10% to 90%)
            - Number of elements in series.

            Parameters
            ----------
            array : np.array of shape(n_samples,)
                Array of lengths.

            Returns
            -------
            result : list
                List of features described above.
            """
        # Get data as pandas Series
        df = pd.Series(array)
        # Compute features data
        return [
            df.min(),
            df.max(),
            df.mean(),
            df.mad(),
            df.std(),
            df.var(),
            df.skew(),
            df.kurtosis(),
            np.percentile(array, 10) if array.shape[0] else 0,
            np.percentile(array, 20) if array.shape[0] else 0,
            np.percentile(array, 30) if array.shape[0] else 0,
            np.percentile(array, 40) if array.shape[0] else 0,
            np.percentile(array, 50) if array.shape[0] else 0,
            np.percentile(array, 60) if array.shape[0] else 0,
            np.percentile(array, 70) if array.shape[0] else 0,
            np.percentile(array, 80) if array.shape[0] else 0,
            np.percentile(array, 90) if array.shape[0] else 0,
            df.shape[0]
        ]
