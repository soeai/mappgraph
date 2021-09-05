# Enhanced_Flowprint

This code was implemented as part of the MAppGraph [1] paper. It is based on the implementation of Flowprint [2]. There are some new functions in the code compared to the original version. I also implement to run in parallel to increase performance.

The original implementation of FlowPrint is available on https://github.com/Thijsvanede/FlowPrint.

# Introduction

Our dataset is very large compared to the dataset used in Flowprint paper. So, we split data into small chunks, to train different models. Each models will be trained, and preditct independently. After all, we predict by combine all the models using voting technique.

We have splited in different traffic duration and overlap time. Naming convention is WindowsSize_Overlap. We have 5 folder, corresponding with 1_0, 2_0, 3_1, 4_2, and 5_3. In each folder, we have one zip file for training data and one for testing data.

Preprocessed data is available at:
* 1_0 and 2_0: https://drive.google.com/drive/folders/113i9dXp7WRnOU68isneAgI0J1cUUISlD?usp=sharing.
* 3_1: https://drive.google.com/drive/folders/1DV1jdM-hAh6nnZ_9WpUd6vlx8udc7wbW?usp=sharing.
* 4_2: https://drive.google.com/drive/folders/1jk4jTNFrJwylzlHtBdXvoED4U0M2kAoM?usp=sharing.
* 5_3: https://drive.google.com/drive/folders/1KwkOYS-yKOe2DcdbjcS1cbXxuj5psqOm?usp=sharing.

# Train

To train models, you must first download the training data set. The training data set should be put into the train_data directory. To start training, run the file train_models.py. The train results will be saved to the models folder.
```
python train_models.py
```

From line 50 to 55, you can modify Flowprint configuration like batch, windows size, correlation, or similarity.
```
flowprint = FlowPrint(
    batch       = 300,
    window      = 10,
    correlation = 0.1,
    similarity  = 0.9
)
```

In the paper, we did try window size of 1, 5, and 10. We see that the result is best at 10, so we use window size of 10 as default.

By default, program will run in parallel, with number of thread is half of number of CPU threads. You can modify it by changing NUMBER_OF_PROCESSED variable.

# Test

To test, we first download the testing data set. The testing data set is placed in the test_data folder.
We run the file test_models.py to start the test. The prediction results of the models, the predictions for each sample are saved separately, in the prediction folder.
```
python test_models.py
```

By default, program will run in parallel, with number of thread is half of number of CPU threads. You can modify it by changing NUMBER_OF_PROCESSED variable.

After having prediction of models, we combine them by voting. We run file voting.py to vote. voting.py will create a folder inside predict folder, contain prediction of voting all available model prediction.
```
python voting.py
```

To have a summary of precision, recall, f1, and accuracy of each model, and voting, we run file print_results.py, those summary will print to the console.
```
python print_results.py
```


# References
[1] `Thai-Dien Pham, Thien-Lac Ho, Tram Truong-Huu, Tien-Dung Cao, Hong-Linh Truong, “MAppGraph: Mobile-App Classification on Encrypted Network Traffic using Deep Graph Convolution Neural Networks”, Annual Computer Security Applications Conference - ACSAC, December 6-10, 2021.`

[2] `van Ede, T., Bortolameotti, R., Continella, A., Ren, J., Dubois, D. J., Lindorfer, M., Choffnes, D., van Steen, M. & Peter, A. (2020, February). FlowPrint: Semi-Supervised Mobile-App Fingerprinting on Encrypted Network Traffic. In 2020 NDSS. The Internet Society.`
