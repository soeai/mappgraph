### Introduction

This page introduces the work of the Encrypted Network Traffic Classification using Deep Learning project from School of Engineering, Tan Tao University. In this project, we develop a method for processing network traffic and generating graphs with node features and edge weights that better represent the communication behavior of mobile apps. After that, DGCNN model is used to learn the communication behavior of mobile apps from a large number of graphs. This model achieves very high performance in mobile-app classification.

### Data

We collect mobile traffic for 101 mobile apps. For each app, more than 30 hours of traffic is collected.

The mobile traffic is saved in a folder named *source* as csv files. Inside this folder, there are 101 sub-folder. Each sub-folder represents for one app and contains the mobile traffic of that app. Duration of mobile traffic in different files is different (min: 4.664 minutes, max: 465.7 minutes, mean: 101.573 minutes). The structure of *source* folder is shown as below.

![GitHub Logo](/images/sources.png)

### Guide

#### 1. Generate mobile traffic chunks with the same length

![GitHub Logo](/images/splitting_chunks.png)

As the image above, a big mobile traffic chunk (saved as a cvs file) is splitted into many small chunks with the same length. There are two hyper-paramters here:

* Duration (T): Length of each traffic chunk after generating.
* Overlap: Use for data augmentation.

There are 5 set of hyper-parameters (Duration – T and Overlap):

<table>
    <thead>
        <tr>
            <th>Hyper-parameters</th>
            <th>set1</th>
            <th>set2</th>
            <th>set3</th>
            <th>set4</th>
            <th>set5</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Duration - T (minutes)</td>
            <td>5</td>
            <td>4</td>
            <td>3</td>
            <td>2</td>
            <td>1</td>
        </tr>
        <tr>
            <td>Overlap (minutes)</td>
            <td>3</td>
            <td>2</td>
            <td>1</td>
            <td>0</td>
            <td>0</td>
        </tr>
    </tbody>
</table>

Running notebook *“generating_samples.ipynb”* to create the mobile traffic chunks with the same length. We need to input a set of hyper-parameters (duration, overlap) at the beginning of the notebook. After running the notebook with 5 set of hyper-parameters, the result will be saved as the image below:

![GitHub Logo](/images/samples.png)

For each set of hyper-paramters, there is a folder named *samples* that contain the mobile traffic chunks. 

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
            <td rowspan=5>10</td>
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
        <tr>
            <td>4</td>
            <td rowspan=4>20</td>
            <td rowspan=4>10</td>
        </tr>
         <tr>
            <td>3</td>
        </tr>
         <tr>
            <td>2</td>
        </tr>
         <tr>
            <td>1</td>
        </tr>
    </tbody>
</table>

The graphs are saved in the structure as below:

![GitHub Logo](/images/graphs.png)

All graphs of one app with a specific set of parameters are saved in 2 csv files (features.csv and weights.csv). In both two files, there is a column named *graph_id* to distinguish between different graphs.

#### 4. Running experiments

So far, we already have graphs generated for all parameters (N and T). Next step is running notebook *“train_GNN.ipynb”* to train the Graph Neural Network and do prediction on the testing dataset.

There are 6 hyper-parameters we need to choose before running the notebook. Each set of hyper-parameters will correspond to one experiment.

List of hyper-parameters:
* N: The maximum nodes kept to build a graph.
* t: Slide duration, used to compute weight between 2 nodes.
* k: A hyper-parameter defined in GNN architecture.
* T: Duration of mobile traffic used to generate a graph.
* apps: List of apps we want to classify.
* features: List of features of each node used to classify.

##### All experiments with MAppGraph presented in the paper:
##### **_1. Impact of Number of Graph Nodes used to Train Models_**
<table>
    <thead>
        <tr>
            <th>N</th>
            <th>t (seconds)</th>
            <th>k</th>
            <th>T (minutes)</th>
            <th>apps</th>
            <th>features</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>7</td>
            <td rowspan=4>10</td>
            <td>7</td>
            <td rowspan=4>5</td>
            <td rowspan=4>List of 101 apps</td>
            <td rowspan=4>List of all 63 features</td>
        </tr>
        <tr>
            <td>10</td>
            <td>10</td>
        </tr>
        <tr>
            <td>20</td>
            <td>20</td>
        </tr>
        <tr>
            <td>30</td>
            <td>30</td>
        </tr>
    </tbody>
</table>

##### **_2. Impact of Time Window Duration of Traffic Collection for Graph Construction_**
<table>
    <thead>
        <tr>
            <th>N</th>
            <th>t (seconds)</th>
            <th>k</th>
            <th>T (minutes)</th>
            <th>apps</th>
            <th>features</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=5>20</td>
            <td rowspan=5>10</td>
            <td rowspan=5>10</td>
            <td>5</td>
            <td rowspan=5>List of 101 apps</td>
            <td rowspan=5>List of all 63 features</td>
        </tr>
        <tr>
            <td>4</td>
        </tr>
        <tr>
            <td>3</td>
        </tr>
        <tr>
            <td>2</td>
        </tr>
        <tr>
            <td>1</td>
        </tr>
    </tbody>
</table>

##### **_3. Impact of Slice Duration on Cross-Correlation in Graph Construction_**
<table>
    <thead>
        <tr>
            <th>N</th>
            <th>t (seconds)</th>
            <th>k</th>
            <th>T (minutes)</th>
            <th>apps</th>
            <th>features</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=3>20</td>
            <td>1</td>
            <td rowspan=3>10</td>
            <td rowspan=3>5</td>
            <td rowspan=3>List of 101 apps</td>
            <td rowspan=3>List of all 63 features</td>
        </tr>
        <tr>
            <td>5</td>
        </tr>
        <tr>
            <td>10</td>
        </tr>
    </tbody>
</table>

##### **_4. Performance with and without using the IP Addresses in Feature Vectors_**
<table>
    <thead>
        <tr>
            <th>N</th>
            <th>t (seconds)</th>
            <th>k</th>
            <th>T (minutes)</th>
            <th>apps</th>
            <th>features</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=2>20</td>
            <td rowspan=2>10</td>
            <td rowspan=2>10</td>
            <td rowspan=2>5</td>
            <td rowspan=2>List of 101 apps</td>
            <td>List of all 63 features</td>
        </tr>
        <tr>
            <td>List of 59 features (without IP features)</td>
        </tr>
    </tbody>
</table>

##### **_5. Classification of Mobile Apps with Similar Functionalities_**
<table>
    <thead>
        <tr>
            <th>N</th>
            <th>t (seconds)</th>
            <th>k</th>
            <th>T (minutes)</th>
            <th>apps</th>
            <th>features</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=2>20</td>
            <td rowspan=2>10</td>
            <td rowspan=2>10</td>
            <td rowspan=2>5</td>
            <td>List of 17 similar apps</td>
            <td rowspan=2>List of all 63 features</td>
        </tr>
        <tr>
            <td>List of 17 different apps</td>
        </tr>
    </tbody>
</table>

* List of 17 similar apps: *'diijam', 'myradio', 'spotify', 'nhaccuatui', 'soundcloud', 'sachnoiapp', 'truyenaudiosachnoiviet', 'voizfm', 'tunefm', 'radiofm', 'nhacvang', 'wesing', 'kaka', 'podcast_player', 'starmarker', 'zingmp3', 'truyenaudio'*
* List of 17 different apps: *'zingmp3', 'fptplay', 'baomoi', 'nimotv', 'messenger', 'tiki', 'facebook', 'lienquan_mobile', 'quora', 'among_us', 'azar', 'tiktok', 'medoctruyen', 'weeboo', 'tinder', 'hago', 'bida'*

##### **_6. Performance with Different Number of Apps_**

<table>
    <thead>
        <tr>
            <th>N</th>
            <th>t (seconds)</th>
            <th>k</th>
            <th>T (minutes)</th>
            <th>apps</th>
            <th>features</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=10>20</td>
            <td rowspan=10>10</td>
            <td rowspan=10>10</td>
            <td rowspan=10>5</td>
            <td>List of 10 apps</td>
            <td rowspan=10>List of all 63 features</td>
        </tr>
        <tr>
            <td>List of 20 apps</td>
        </tr>
        <tr>
            <td>List of 30 apps</td>
        </tr>
        <tr>
            <td>List of 40 apps</td>
        </tr>
        <tr>
            <td>List of 50 apps</td>
        </tr>
        <tr>
            <td>List of 60 apps</td>
        </tr>
        <tr>
            <td>List of 70 apps</td>
        </tr>
        <tr>
            <td>List of 80 apps</td>
        </tr>
        <tr>
            <td>List of 90 apps</td>
        </tr>
        <tr>
            <td>List of 101 apps</td>
        </tr>
    </tbody>
</table>

* The list of 10, 20, 30, 40, 50, 60, 70, 80, 90, 101 apps can be found in [apps_list.txt](https://github.com/soeai/MAppGraph/blob/gh-pages/apps_list.txt).
* The list of apps is chosen randomly from 101 apps. 

### Artifact Verification
* Due to limitation of storage space, we only provide the processed datasets of two cases in Table 4 of the paper corresponding to T_window = 5 and 2. The other optimal hyper-parameters are N = 20, k = 10, t = 10s (all features of node are used). The number of classification app is 101. You can run the notebook *"train_GNN.ipynb"* (using Google Colab or GPU computer ) with the default configution of the hyper-parameters (T=5, N=20, k=20, t=10s) on [DATA T5_3](https://github.com/soeai/MAppGraph/tree/gh-pages/data/5_3). 
* For the second case (i.e., T=2, N=20, k=20, t=10s), please change the parameter T = 2 as well as Overlap = 0 in Config Seting section to work with [DATA T2_0](https://github.com/soeai/MAppGraph/tree/gh-pages/data/2_0).
* To run other experiments, you need to follow all steps in this guide section to generate data again and run the notebook *"train_GNN.ipynb"* with different config setting. Data is available if requested.

### Raw Data
* The .pcap files are also provided in contact with individual agreement.

### Publications

1. Thai-Dien Pham, Thien-Lac Ho, Tram Truong-Huu, Tien-Dung Cao, Hong-Linh Truong, "MAppGraph: Mobile-App Classification on Encrypted Network
Traffic using Deep Graph Convolution Neural Networks", Annual Computer Security Applications Conference - ACSAC'2021 (Accepted).

### Support or Contact

For any query or issue, please contact dung.cao@ttu.edu.vn
