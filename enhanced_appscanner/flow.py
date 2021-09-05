import ipaddress
import numpy as np

class Flow(object):

    def extract(self, bursts):
        """Extract flows from bursts.

            Parameters
            ----------
            bursts : list of bursts
                Each entry in list should contain a numpy array containing
                packets of burst.

            Returns
            -------
            result : dict
                Dictionary of flow_key -> packet lengths.
                Flow tuple is defined as (timestamp, src, sport, dst, dport)
                Packet lengths are positive for outgoing messages
                and negative if incoming messages.
            """
        # Initialise result
        result = dict()

        # Loop over bursts
        for burst in bursts:
            # Add single burst to result
            
            if burst.shape[0] > 0:
                result.update(self.extract_single(burst))

        # Return result
        return result


    def extract_single(self, burst):
        """Extract flows from single burst.

            Parameters
            ----------
            burst : np.array of shape=(n_samples, n_features)
                Numpy array containing packets of burst.

            Returns
            -------
            result : dict
                Dictionary of flow_tuple -> packet lengths.
                Flow tuple is defined as (timestamp, src, sport, dst, dport)
                Packet lengths are positive for outgoing messages
                and negative if incoming messages.
            """
        # Initialise result
        result = dict()

        # Extract burst timestamp
        timestamp = float(burst[0, 0])

        # Loop over packets in burst
        for packet in burst:
            # Define key as 5-tuple (burst, src, sport, dst, dport)
            key, incoming = self.key(timestamp, packet)

            # Set length depending on incoming or outgoing
            length = -packet[5] if incoming else packet[5]

            # Add length of packet to flow
            result[key] = result.get(key, []) + [length]

        # Convert lengths to numpy array.
        result = {k: np.array(v) for k, v in result.items()}

        # Return result
        return result


    def key(self, timestamp, packet):
        """Extract the key of a packet and check whether it is incoming or
           outgoing.

            Parameters
            ----------
            timestamp : float
                Timestamp of burst.

            packet : np.array of shape=(n_features)
                Packet representation [timestamp, src, dst, sport, dport, len]

            Returns
            -------
            key : tuple
                Key tuple of flow.

            incoming : boolean
                Boolean indicating whether flow is incoming.
            """
        # Define key as 5-tuple (burst, src, sport, dst, dport)
        key = (timestamp, ipaddress.ip_address(int(packet[1])), packet[3],
                          ipaddress.ip_address(int(packet[2])), packet[4])

        # Check if flow message is incoming
        incoming = key[3].is_private

        # If incoming, return incoming key
        if incoming:
            key = (key[0], key[3], key[4], key[1], key[2])

        # Set IP addresses to string
        key = (key[0], str(key[1]), key[2], str(key[3]), key[4])

        # Return result
        return key, incoming
