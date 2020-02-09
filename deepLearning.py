import pandas as pd
import numpy as np
import os
import librosa


def classname_extractor(filename):
    """
    function for extracting first part (until '_' letter) of filename,
    as a name of class for deep learning process
    :param filename:    name of wav file
    :return:            string with first part of filename
    """
    index = 0
    i = 0
    class_name = []
    for letter in filename:
        if letter is '_':
            if index != 0:
                class_name = filename[:index]
                return class_name
            else:
                print("Brak nazwy klasy obiektu audio!!!")
                break
        index += 1
    return -1

def extract_features(file_name):

    try:
        audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        mfccsscaled = np.mean(mfccs.T ,axis=0)
    except:
        print("Error encountered while parsing file: ")
        return None

    return mfccsscaled



# Set the path to the full UrbanSound dataset
fulldatapath = '/Urban Sound/UrbanSound8K/audio/'

metadata = pd.read_csv(fulldatapath + '../metadata/UrbanSound8K.csv')

features = []

# Iterate through each sound file and extract the features
for index, row in metadata.iterrows():
    file_name = os.path.join(os.path.abspath(fulldatapath), 'fold' + str(row["fold"]) + '/',
                             str(row["slice_file_name"]))

    class_label = row["class_name"]
    data = extract_features(file_name)

    features.append([data, class_label])

# Convert into a Panda dataframe
featuresdf = pd.DataFrame(features, columns=['feature', 'class_label'])

print('Finished feature extraction from ', len(featuresdf), ' files')