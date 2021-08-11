## Introduction

This page introduces the work of the Encrypted Network Traffic Classification using Deep Learning project from School of Engineering, Tan Tao University. In this project, we develop a method for processing network traffic and generating graphs with node features and edge weights that better represent the communication behavior of mobile apps. After that, DGCNN model is used to learn the communication behavior of mobile apps from a large number of graphs. This model achieves very high performance in mobile-app classification.

### Data

We collect mobile traffic for 101 mobile apps. For each app, the number of times that we collect is about 30 hours.

The mobile traffic is saved in folder named *source* as csv files. Inside this folder, there are 101 sub-folder. Each sub-folder represent for one app and contains mobile traffic of that app. Duration of mobile traffic in different files are different (min: 4.664 minutes, max: 465.7 minutes, mean: 101.573 minutes). The structure of source folder is showed as below.

![GitHub Logo](/images/source.png)

### Guide

#### 1. Generate mobile traffic chunks with the same length

![GitHub Logo](/images/splitting_chunks.png)

As the image above, a big mobile traffic chunk (saved as a cvs file) is splitted into many small chunks with the same length. There are two hyper-paramters here:

* Duration (T): Length of each traffic chunk after generating.
* Overlap: Use for data augmentation.

There are 5 set of hyper-parameters (Duration – T and Overlap):
Duration - T (minutes) | 5 | 4 | 3 | 2 | 1
Overlap | 3 | 2 | 1 | 0 | 0

### Publications

1. Thai-Dien Pham, Thien-Lac Ho, Tram Truong-Huu, Tien-Dung Cao, Hong-Linh Truong, "MAppGraph: Mobile-App Classification on Encrypted Network
Traffic using Deep Graph Convolution Neural Networks", submitted to ACSAC2021.

### Support or Contact

For any query or issue, please contact dung.cao@ttu.edu.vn
