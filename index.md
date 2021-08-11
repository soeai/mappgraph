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
Hyper-parameters  | set1 | set2 | set3 | set4 | set5 
------------ | ------------- | ------------ | ------------- | ------------ | ------------- 
Duration - T (minutes) | 5 | 4 | 3 | 2 | 1
Overlap | 3 | 2 | 1 | 0 | 0

Running notebook *“generating_samples.ipynb”* to create the mobile traffic chunks with the same length. We need to input a set of hyper-parameters (duration, overlap) at the beginning of the notebook. After running the notebook with 5 set of hyper-parameters, the result will be saved as the image below:

![GitHub Logo](/images/samples.png)

For each set of hyper-paramters, there is a folder named samples that contain the mobile traffic chunks. 

#### 2. Train-test split

Running notebook *“generating_train_test.ipynb”* to split the data into training and testing data. The training size is 0.8. For each app, there is 0.8 of samples for training and 0.2 for testing. After running the notebook, the information of training and testing sampls is saved in a json file *“train_test_info.json”*

The structure of a json file:
{ app1: (list of filenames of training samples, list of filenames of testing samples), app2: …… }

Because there are 5 set of parameters, we will have 5 files *‘train_test_info.json’*. They are saved as image below.

![GitHub Logo](/images/train_test.png)

#### 3. Generating graphs from traffic chunks

Running notebook *“generating_graphs.ipynb”* to convert all traffic chunks into graphs and save all of the graphs in 2 folder train_graphs and test_graphs (training and testing samples are determined by *‘train_test_info.json’*).

There are two more hyper-parameters we need to input in the notebook before generating graphs. (N and window t). Each set of hyper-parameters (N, t) will also produce different set of graphs. 

The combination of all parameters we use to run experiments:

<table>
    <thead>
        <tr>
            <th>Duration-T (minutes)</th>
            <th>N</th>
            <th>t (seconds)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=7>5</td>
            <td>7</td>
            <td rowspan=4>10</td>
        </tr>
        <tr>
            <td>10</td>
        </tr>
        <tr>
            <td>20</td>
        </tr>
        <tr>
            <td>30</td>
        </tr>
        <tr>
            <td>10000</td>
        </tr>
        <tr>
            <td rowspan=2>20</td>
            <td>5</td>
        </tr>
        <tr>
            <td>1</td>
        </tr>
    </tbody>
</table>

### Publications

1. Thai-Dien Pham, Thien-Lac Ho, Tram Truong-Huu, Tien-Dung Cao, Hong-Linh Truong, "MAppGraph: Mobile-App Classification on Encrypted Network
Traffic using Deep Graph Convolution Neural Networks", submitted to ACSAC2021.

### Support or Contact

For any query or issue, please contact dung.cao@ttu.edu.vn
