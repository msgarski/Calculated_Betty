import pandas as pd
import numpy as np
import os
import librosa
import soundfile as sf
from scipy.io.wavfile import read, write
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Convolution2D, Conv2D, MaxPooling2D, GlobalAveragePooling2D
from tensorflow.keras.callbacks import ModelCheckpoint
from datetime import datetime
from tensorflow.keras.optimizers import Adam
from keras.utils import np_utils
from sklearn import metrics

def final_checking_samples(path_to_folder):
    try:
        file_list = os.listdir(path_to_folder)  # getting list of files from declared path with samples
        #print(file_list)
    except:
        print("nie otwiera folderu????")
    for nazwa in file_list:
        single_file_path = os.path.join(path_to_folder, nazwa)
        audio, sample_rate = librosa.load(single_file_path, res_type='kaiser_fast')
        try:
            ob = sf.SoundFile(single_file_path)
        except:
            print("Nie udało się otworzyć pliku do sprawdzenia")
        print(nazwa, "  ")
        print('Sample rate: {}'.format(ob.samplerate))
        print(" sample_rate: ", sample_rate)
        print(' Channels: {}'.format(ob.channels))
        print(' Subtype: {}'.format(ob.subtype))
        print('\n')

def classname_extractor(file_name):
    """
    function for extracting first part (until '_' letter) of filename,
    as a name of class for deep learning process
    :param filename:    name of wav file
    :return:            string with first part of filename
    """
    index = 0
    i = 0
    class_name = []
    for letter in file_name:
        if letter is '_':
            if index != 0:
                class_name = file_name[:index]
                return class_name
            else:
                print("Brak nazwy klasy obiektu audio!!!")
                break
        index += 1
    return -1

def extract_features(file_name):
    try:
        # todo librosa oszukuje na sample rate, inne dają 2x więcej
        audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
        mfccs_spectrogram = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        #print("mfccs: ", mfccs_spectrogram.shape)
        #mfccsscaled = np.mean(mfccs_spectrogram.T, axis=0)  # todo może spektrogram od innych?
        #print("mfccsscaled: ", mfccsscaled.shape)
    except:
        print("Error encountered while parsing file: ")
        return None
    return mfccs_spectrogram

def prepare_wav(filepath):
    a = read(filepath)
    audio = np.array(a[1], dtype=np.int16)
    sample_rate = 44100
    try:
        # todo librosa oszukuje na sample rate, inne dają 2x więcej
        #audio, sample_rate = librosa.load(file_name, res_type='kaiser_fast')
        mfccs_spectrogram = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
        mfccsscaled = np.mean(mfccs_spectrogram.T ,axis=0) # todo może spektrogram od innych?
    except:
        print("Error encountered while parsing file: ")
        return None
    return mfccs_spectrogram

def padding_audio(ys, sek, frame_rate):
    length = len(ys)
    print("dlugosc przed: ", length)
    desired_legth = sek * frame_rate
    difference = desired_legth - length
    if difference > 0:
        print("roznica: ",difference)
        ys = np.pad(ys, (0, difference), 'constant')
    else:
        ys = ys[:desired_legth]
    print("dlugosc po: ", len(ys))
    return ys


path_to_folder = os.getcwd()
data_folder = 'learning_data'
#data_folder = 'nagrania/records_calculator'
#test_file = 'nagrania'
fulldatapath = os.path.join(path_to_folder, data_folder)

"""
a = read(test_file)
data = np.array(a[1],dtype=np.int16)
data = padding_audio(data, 2, 44100)
"""
model = tf.keras.models.load_model("weights_best_cnn.hdf5")

try:
    file_list = os.listdir(fulldatapath)                       # getting list of files from declared path with samples
    print(file_list)
except:
    print("nie otwiera folderu????")

for nazwa in file_list:
    single_file_path = os.path.join(fulldatapath, nazwa)        # exact absolute path to file from list
    if os.path.isfile(single_file_path):
        label = classname_extractor(nazwa)
        data = extract_features(single_file_path)

        x = data.reshape(1, data.shape[0], data.shape[1], 1)
        prediction = model.predict(x)
        #clas = model.predict_classes(x)
        max_clas = np.argmax(prediction)
        #print(prediction)
        print("nazwa klasy: ")
        #print(clas)
        print(max_clas)
        print("\t%s ==> %d" % (label, max_clas))

print("koniec")




