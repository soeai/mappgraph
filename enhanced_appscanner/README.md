# Enhanced_Appscanner
This code was implemented as part of the MAppGraph [1] paper. It is based on the implementation of Single Large Random Forest Classifier of AppScanner [2]. There are some new functions in the code compared to the original version.

The original implementation of Single Large Random Forest Classifier of AppScanner is available on https://github.com/Thijsvanede/AppScanner.

## Introduction
Appscanner is a method for mobile traffic classification based on flows. They define flows in mobile traffic and use a Machine Learning model to classify flows among different apps. But for our approach - MAppGraph, we capture mobile traffic chunks in a specific duration of time (say 5 minutes) and classify them. To solve our problem by Appscanner method, we use a voting scheme. Many flows are extracted from a mobile traffic chunk. After that, the label of each flow is predicted by Appscanner method. Finally, the voting scheme is used to conclude the final label of the traffic chunk.

Moreover, our dataset is very large compared to the dataset used in  Appscanner paper. So, we can build 16 different Machine Learning models. Each model is trained on a different dataset. A mobile traffic chunk will be predicted by 16 models. After that, the voting scheme is also used here to get the final result.

## Dataset
For training, there are 16 small datasets. For each small dataset, there are 101 mobile traffic chunks of 101 apps. The duration of one mobile traffic chunk is 50 minutes. With this dataset, we can train 16 different models. For testing, there is a dataset including mobile traffic chunks (in 5 minutes) of 101 apps. Each app has about 100-300 traffic chunks to test.

The dataset is saved in 2 folders *appscanner_models* and *test*. The file structure is shown as the following:
```
Appscanner_voting
|
├── appscanner_models
│   ├── model_1
|   |    └── data
|   ├── model_2
|   |    └── data
|   ...
|
├── test
|   ├── among_us
|   ├── animal_restaurant
|   ...
|
├── predictions
│   ├── model_1
|   ├── model_2
|   ...
|
├── __init__.py
├── apps.json
├── appscanner.py
├── burst.py
├── features.py
├── flow.py
├── predict.py
├── preprocessor.py
├── print_result.py
├── reader.py
├── train.py
└── voting.py

```

## Train
For training, run:
```
python train.py --app_number x
```
x could be 10, 20, 30, 40, 50, 60, 70, 80, 90, 101. It is the number of apps we want to train and test. The list of apps is saved in *apps.json* file. In the paper of MAppGraph, we run with all different number of apps to see the change of performance. After running, the 16 models will be trained and saved in the folder *appscanner_models*. They will be used for testing later.

## Test
First, we run:
```
python predict.py --app_number x
```
x is still the number of apps. We have to use the same x for training and testing. After running, the testing result will be saved in a folder named *predictions*. There will be 16 sub-folders in *predictions*. Each folder contains the prediction result of one model. 

After having the prediction result of all 16 individual models, we run:
```
python voting.py
```
This step is to get the final prediction result by voting scheme. The final result of voting scheme will be save in *predictions* folder as *model_17*.

Finally, we run:
```
python print_result.py
```
It will show the precision, recall, f1-score, accuracy of 17 models (including the voting model).

## References
[1] `Thai-Dien Pham, Thien-Lac Ho, Tram Truong-Huu, Tien-Dung Cao, Hong-Linh Truong, “MAppGraph: Mobile-App Classification on Encrypted Network Traffic using Deep Graph Convolution Neural Networks”, Annual Computer Security Applications Conference - ACSAC, December 6-10, 2021.`

[2] `Taylor, V. F., Spolaor, R., Conti, M., & Martinovic, I. (2016, March). Appscanner: Automatic fingerprinting of smartphone apps from encrypted network traffic. In 2016 IEEE European Symposium on Security and Privacy (EuroS&P) (pp. 439-454). IEEE.`
