# MAppGraph
Encrypted Network Traffic Classification using Deep Learning
This repository contains the code for FlowPrint by the authors of the NDSS FlowPrint [1] paper [[PDF]](https://dx.doi.org/10.14722/ndss.2020.24412).
Please [cite](#References) FlowPrint when using it in academic publications.
This `master` branch provides FlowPrint as an out of the box tool.
For the original experiments from the paper, please checkout the `NDSS` branch.

## Introduction
FlowPrint introduces a semi-supervised approach for fingerprinting mobile apps from (encrypted) network traffic.
We automatically find temporal correlations among destination-related features of network traffic and use these correlations to generate app fingerprints.
These fingerprints can later be reused to recognize known apps or to detect previously unseen apps.
The main contribution of this work is to create network fingerprints without prior knowledge of the apps running in the network.

## Documentation
We provide an extensive documentation including installation instructions and reference at [flowprint.readthedocs.io](https://flowprint.readthedocs.io/en/latest/).

## References

### Bibtex
