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

#### 4. Running experiments

So far, we already have graphs generated for all parameters (N and T). Next step is running notebook *“train_GNN.ipynb”* to train the Graph Neural Network and do prediction on the testing dataset.

There are 6 hyper-parameters we need to choose before running the notebook. Each set of hyper-parameters will correspond to one experiment.

List of hyper-parameters:
* N: The maximum nodes kept to build a graph.
* t: Time slide, used to compute weight between 2 nodes.
* k: A hyper-parameter defined in GNN architecture.
* T: Duration of mobile traffic used to generate a graph.
* apps: List of apps we want to classify.
* features: List of features of each node used to classify.

##### All experiments with MAppGraph presented in the paper:
#####*1. Impact of Number of Graph Nodes used to Train Models*
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

*2.	Impact of Time Window Duration of Traffic Collection for Graph Construction*
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

*3.	Impact of Slice Duration on Cross-Correlation in Graph Construction*
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

*4.	Performance with and without using the IP Addresses in Feature Vectors*
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

*5.	Classification of Mobile Apps with Similar Functionalities*
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

*6.	Performance with Different Number of Apps*

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

* List of 10 apps: *'bigo', 'spotify', 'among_us', 'tinder', 'tiktok', 'tiki', 'tuoitre_online', 'hago', 'facebook', 'netflix'*
* List of 20 apps: *'bigo', 'spotify',  'freefire', 'among_us', 'azar', 'comico', 'noveltoon', 'tinder', 'tiktok', 'tiki', 'tuoitre_online',  'wesing', 'hago', 'facebook', 'wikipedia', 'quora', 'snapchat', 'tien_len', 'messenger', 'netflix'*
* List of 30 apps: *'baomoi', 'bigo', 'spotify', 'zingmp3', 'freefire', 'among_us', 'azar', 'comico', 'nimotv', 'noveltoon', 'tinder', 'tiktok', 'tiki', 'tuoitre_online', 'wesing', 'hago', 'facebook', 'wikipedia', 'instagram', 'pinterest', 'quora', 'co_tuong_online', 'ted', 'starmarker', 'snapchat', 'tien_len', 'bida', 'cho_tot', 'messenger', 'netflix'*
* List of 40 apps: *'baomoi', 'bigo', 'spotify', 'nhaccuatui', 'zingmp3', 'freefire', 'among_us', 'azar', 'comico', 'nimotv', 'medoctruyen', 'noveltoon', 'tinder', 'tiktok', 'tiki', 'tuoitre_online', 'bbc_news', 'weeboo', 'wesing', 'hago', 'facebook', 'zoom', 'wikipedia', 'instagram', 'pinterest', 'quora', 'co_tuong_online', 'ted', 'starmarker', 'tango', 'snapchat', 'tien_len', 'bida', 'cho_tot', 'messenger', 'netflix', 'nonolive', 'pubg', 'lienquan_mobile', 'reddit'*
* List of 50 apps: *'baomoi', 'fptplay', 'bigo', 'spotify', 'nhaccuatui', 'soundcloud', 'zingmp3', 'freefire', 'among_us', 'azar', 'comico', 'nimotv', 'medoctruyen', 'noveltoon', 'tinder', 'tiktok', 'tiki', 'lotus', 'tuoitre_online', 'bbc_news', 'twitter', 'weeboo', 'topcv', 'wesing', 'hago', 'google_meet', 'facebook', 'zoom', 'wikipedia', 'instagram', 'pinterest', 'quora', 'chess', 'co_tuong_online', 'ted', 'starmarker', 'tango', 'snapchat', 'tien_len', 'bida', 'cho_tot', 'messenger', 'netflix', 'nonolive', 'pubg', 'lienquan_mobile', 'likee_lite', 'reddit', 'sendo', 'ola_party'*
* List of 60 apps: *'baomoi', 'fptplay', 'bigo', 'spotify', 'nhaccuatui', 'soundcloud', 'zingmp3', 'freefire', 'among_us', 'azar', 'comico', 'nimotv', 'mangatoon', 'medoctruyen', 'noveltoon', 'vtvgo', 'tinder', 'tiktok', 'linkedin', 'tiki', 'tinhte', 'lotus', 'tuoitre_online', 'vietnamworks', 'bbc_news', 'twitter', 'weeboo', 'twitch', 'topcv', 'toc_chien', 'wesing', 'hago', 'google_meet', 'dubsmash', 'facebook', 'zoom', 'wikipedia', 'instagram', 'pinterest', 'quora', 'chess', 'co_tuong_online', 'ted', 'starmarker', 'skype', 'tango', 'snapchat', 'tien_len', 'animal_restaurant', 'bida', 'cho_tot', 'messenger', 'netflix', 'nonolive', 'pubg', 'lienquan_mobile', 'likee_lite', 'reddit', 'sendo', 'ola_party'*
* List of 70 apps: *'baomoi', 'fptplay', 'bigo', 'spotify', 'nhaccuatui', 'soundcloud', 'wetv', 'zingmp3', 'freefire', 'among_us', 'azar', 'comico', 'nimotv', 'mangatoon', 'medoctruyen', 'noveltoon', 'vtvgo', 'tinder', 'tiktok', 'linkedin', 'tiki', 'tinhte', 'lotus', 'tuoitre_online', 'vietnamworks', 'wallstreet_journal', 'bbc_news', 'twitter', 'weeboo', 'twitch', 'vnexpress', 'topcv', 'toc_chien', 'wesing', 'hago', 'google_meet', 'dubsmash', 'facebook', 'hahalolo', 'hello_yo', 'zoom', 'wikipedia', 'instagram', 'jobway', 'pinterest', 'quora', 'lazada', 'chess', 'cake', 'mobile_legend', 'co_tuong_online', 'ted', 'telegram', 'starmarker', 'skype', 'tango', 'snapchat', 'tien_len', 'animal_restaurant', 'bida', 'cho_tot', 'messenger', 'netflix', 'nonolive', 'pubg', 'lienquan_mobile', 'likee_lite', 'reddit', 'sendo', 'ola_party'*
* List of 80 apps: *'baomoi', 'fptplay', 'bigo', 'myradio', 'spotify', 'nhaccuatui', 'soundcloud', 'wetv', 'zingmp3', 'freefire', 'among_us', 'azar', 'comico', 'nimotv', 'mangatoon', 'medoctruyen', 'noveltoon', 'vtvgo', 'tivi24h', 'tinder', 'tivi360', 'tiktok', 'linkedin', 'tiki', 'tinhte', 'lotus', 'tuoitre_online', 'vietnamworks', 'wallstreet_journal', 'bbc_news', 'twitter', 'weeboo', 'twitch', 'vnexpress', 'topcv', 'toc_chien', 'wesing', 'hago', 'google_meet', 'dubsmash', 'facebook', 'hahalolo', 'zalo', 'hello_yo', 'zoom', 'wikipedia', 'instagram', 'jobway', 'kaka', 'pinterest', 'quora', 'lazada', 'chess', 'cake', 'mobile_legend', 'co_tuong_online', 'ted', 'telegram', 'starmarker', 'skype', 'tango', 'thanhnien', 'snapchat', 'tien_len', 'animal_restaurant', 'bida', 'cho_tot', 'messenger', 'netflix', 'nonolive', 'podcast_player', 'pubg', 'partying', 'lienquan_mobile', 'likee_lite', 'reddit', 'sendo', 'shopee', 'the_guardian', 'ola_party'*
* List of 90 apps: *'baomoi', 'fptplay', 'bigo', 'myradio', 'spotify', 'nhaccuatui', 'soundcloud', 'phim247', 'popskid', 'voizfm', 'tunefm', 'wetv', 'zingmp3', 'truyenaudio', 'baohay24h', 'freefire', 'among_us', 'azar', 'comico', 'nimotv',
 'mangatoon', 'medoctruyen', 'noveltoon', 'tivi247', 'vtvgo', 'tivi24h', 'tinder', 'tinmoi24h', 'tivi360', 'tiktok', 'linkedin', 'tiki', 'tinhte', 'lotus', 'tivi_truyentranh_webtoon', 'tuoitre_online', 'vietnamworks', 'wallstreet_journal', 'cnn_news', 'bbc_news', 'twitter', 'weeboo', 'twitch', 'vnexpress', 'topcv', 'toc_chien', 'wesing', 'hago', 'google_meet', 'dubsmash', 'facebook', 'hahalolo', 'zalo', 'hello_yo', 'zoom', 'wikipedia', 'instagram', 'jobway', 'kaka', 'pinterest', 'quora', 'lazada', 'chess', 'cake', 'mobile_legend', 'co_tuong_online', 'ted', 'telegram', 'starmarker', 'skype', 'tango', 'thanhnien', 'snapchat', 'tien_len', 'animal_restaurant', 'bida', 'cho_tot', 'messenger', 'netflix', 'nonolive', 'podcast_player', 'pubg', 'partying', 'lienquan_mobile', 'likee_lite', 'reddit', 'sendo', 'shopee', 'the_guardian', 'ola_party'*
* List of 101 apps: *'diijam', 'baomoi', 'fptplay', 'iQIYI', 'bigo', 'myradio', 'spotify', 'nhaccuatui', 'soundcloud', 'sachnoiapp', 'phim247', 'popskid', 'truyenaudiosachnoiviet', 'vieon', 'voizfm', 'tunefm', 'wetv', 'zingmp3', 'truyenaudio', 'baohay24h', 'freefire', 'among_us', 'azar', 'comico', 'nimotv', 'mangatoon', 'medoctruyen', 'nhacvang', 'noveltoon', 'radiofm', 'tivi247', 'vtvgo', 'tivi24h', 'tinder', 'tinmoi24h', 'tivi360', 'tiktok', 'linkedin', 'tiki', 'tinhte', 'lotus', 'tivi_truyentranh_webtoon', 'tuoitre_online', 'vietnamworks', 'wallstreet_journal', 'cnn_news', 'bbc_news', 'twitter', 'weeboo', 'twitch', 'vnexpress', 'topcv', 'toc_chien', 'wesing', 'hago', 'google_meet', 'dubsmash', 'facebook', 'hahalolo', 'zalo', 'hello_yo', 'dan_tri', 'zoom', 'wikipedia', 'instagram', 'jobway', 'kaka', 'pinterest', 'quora', 'lazada', 'chess', 'cake', 'mobile_legend', 'co_tuong_online', 'ted', 'telegram', 'starmarker', 'skype', 'soha', 'tango', 'thanhnien', 'snapchat', 'tien_len', 'animal_restaurant', 'bida', 'cho_tot', 'messenger', 'netflix', 'nonolive', 'may', 'podcast_player', 'pubg', 'partying', 'kenh14', 'lienquan_mobile', 'likee_lite', 'reddit', 'sendo', 'shopee', 'the_guardian', 'ola_party'*

Note: The list of apps is chosen randomly from 101 apps.


### Publications

1. Thai-Dien Pham, Thien-Lac Ho, Tram Truong-Huu, Tien-Dung Cao, Hong-Linh Truong, "MAppGraph: Mobile-App Classification on Encrypted Network
Traffic using Deep Graph Convolution Neural Networks", submitted to ACSAC2021.

### Support or Contact

For any query or issue, please contact dung.cao@ttu.edu.vn
