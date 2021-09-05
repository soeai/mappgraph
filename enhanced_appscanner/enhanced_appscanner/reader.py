from scapy.all import *
import numpy as np
import ipaddress
import pandas as pd
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import glob
import os
import re
import warnings
from subprocess import Popen, PIPE
from burst import Burst
from flow import Flow
from features import Features



class Reader(object):

    def __init__(self, verbose=False):
        """Reader object for reading packets from .pcap files.

            Parameters
            ----------
            verbose : boolean, default=false
                If True, print which files are being read.
            """
        self.verbose = verbose
    
    def tshark_version(self):
        """Returns the current version of tshark.
            Returns
            -------
            version : string
                Current version number of tshark.
            """
        # Get tshark version via command line
        command  = ["tshark", "--version"]
        process  = Popen(command, stdout=PIPE, stderr=PIPE)
        out, err = process.communicate()

        # Throw error if any
        if err:
            raise ValueError(
                "Exception in tshark version check: '{}'".format(err))

        # Search for version number
        regex   = re.compile('TShark .*(\d+\.\d+\.\d+) ')
        out     = out.decode('utf-8')
        version = regex.search(out).group(1)

        # Return version
        return version
    
    """
        created by Thai-Dien Pham
    """
    def basic_reprocessing(self, df):
        # remove dns protocol
        df = df[(df['source_port'] != 53) & (df['destination_port'] != 53) & 
                (df['source_port'] != 5353) & (df['destination_port'] != 5353) &
                (df['source_port'] != 137) & (df['destination_port'] != 137) &
                (df['source_port'] != 67) & (df['destination_port'] != 67) &
                (df['source_port'] != 68) & (df['destination_port'] != 68) &
                (df['source_port'] != 5355) & (df['destination_port'] != 5355)]
        
        return df

    """
        created by Thai-Dien Pham
    """
    def read_csv(self, path):
        df = pd.read_csv(path, index_col=0)
        df = self.basic_reprocessing(df)


        df = df[['time', 'source_address', 'destination_address', 'source_port', 'destination_port', 'length']]
        df['time'] = df['time'].apply(lambda x: EDecimal(x))
        df['source_address'] = df['source_address'].apply(lambda x: int(ipaddress.ip_address(x.split(',')[0])))
        df['destination_address'] = df['destination_address'].apply(lambda x: int(ipaddress.ip_address(x.split(',')[0])))


        self.packets = np.array(df, dtype=object)

        return self.packets

    """
        created by Thai-Dien Pham
    """
    def read_tshark(self, path):
        """Read TCP and UDP packets from file given by path using tshark backend
            Parameters
            ----------
            path : string
                Path to .pcap file to read.
            Returns
            -------
            result : np.array of shape=(n_packets, n_features)
                Where features consist of:
                0) Timestamp of packet
                1) IP packet source
                2) IP packet destination
                3) TCP/UDP packet source port
                4) TCP/UDP packet destination port
                5) Length of packet
            """
        # Get tshark version
        version = self.tshark_version()
        # Set certificate command based on version
        # tshark versions <3 use ssl.handshake.certificate
        # tshark versions 3+ use tls.handshake.certificate
        certificate  = "ssl" if int(version.split('.')[0]) < 3 else "tls"
        certificate += ".handshake.certificate"

        # Create Tshark command
        command = ["tshark", "-r", path, "-Tfields",
                   "-e", "frame.time_epoch",
                   "-e", "ip.src",
                   "-e", "ip.dst",
                   "-e", "tcp.srcport",
                   "-e", "udp.srcport",
                   "-e", "tcp.dstport",
                   "-e", "udp.dstport",
                   "-e", "ip.len",
                   ]
        # Initialise result
        result = []

        # Call Tshark on packets
        process = Popen(command, stdout=PIPE, stderr=PIPE)
        # Get output
        out, err = process.communicate()

        # Give warning message if any
        if err:
            warnings.warn("Error reading file: '{}'".format(
                err.decode('utf-8')))

        # Read each packet
        for packet in filter(None, out.decode('utf-8').split('\n')):
            # Get all data from packets
            packet = packet.split()

            # Perform check on packets
            if len(packet) < 5: 
                continue

            # Perform check on multiple ip addresses
            packet[1] =  int(ipaddress.ip_address(packet[1].split(',')[0]))
            packet[2] =  int(ipaddress.ip_address(packet[2].split(',')[0]))
            packet[5] = packet[5].replace(',', '')


            # Add packet to result
            result.append([EDecimal(packet[0]), int(packet[1]), int(packet[2]), int(packet[3]), int(packet[4]), int(packet[5])])

        # Get result as numpy array
        self.packets = np.array(result, dtype=object)

        # Check if any items exist
        if not self.packets.shape[0]:
            return np.zeros((0, 5), dtype=object)


        return self.packets

    def read(self, infile):
        """Read TCP packets from input file.
            Parameters
            ----------
            infile : string
                pcap file from which to read packets.
            Returns
            -------
            result : list
                List of packets extracted from pcap file.
                Each packet is represented as a list of:
                 - timestamp
                 - IP source (in byte representation)
                 - IP destination (in byte representation)
                 - TCP source port
                 - TCP destination port
                 - packet length.
            """
        # If verbose, print loading file
        if self.verbose:
            print("Loading {}...".format(infile))

        # Set buffer of packets
        self.packets = []
        # Process packets in infile
        sniff(prn=self.extract, lfilter=lambda x: TCP in x, offline=infile)

        # Convert to numpy array
        self.packets = np.array(self.packets)
        # In case of packets, sort on timestamp
        if self.packets.shape[0]:
            # Sort based on timestamp
            self.packets = self.packets[self.packets[:, 0].argsort()]

        # Return extracted packets
        return self.packets


    def extract(self, packet):
        """Extract relevant fields from given packet and adds it to globel
           self.packets variable.

            Parameters
            ----------
            packet : scapy.IP
                Scapy IP packet extracted by sniff function.
            """
        # Extract relevant content from packet
        data = [packet.time,
                int(ipaddress.ip_address(packet["IP"].src)),
                int(ipaddress.ip_address(packet["IP"].dst)),
                packet["TCP"].sport,
                packet["TCP"].dport,
                packet["IP"].len]
        # Add packet to buffer
        self.packets.append(data)