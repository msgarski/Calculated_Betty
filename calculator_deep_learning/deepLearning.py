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
        #mfccsscaled = np.mean(mfccs_spectrogram.T ,axis=0) # todo może spektrogram od innych?
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
    return ys

# Set the path to the full UrbanSound dataset
path_to_folder = os.getcwd()
#data_folder = 'nagrania/learning_data'     # my path
data_folder = 'learning_data'               # path for git
#test_file = 'nagrania/'
fulldatapath = os.path.join(path_to_folder, data_folder)


features = []
try:
    file_list = os.listdir(fulldatapath)                       # getting list of files from declared path with samples
    print(file_list)
except:
    print("nie otwiera folderu????")

for nazwa in file_list:
    single_file_path = os.path.join(fulldatapath, nazwa)        # exact absolute path to file from list
    if os.path.isfile(single_file_path):
        class_label = classname_extractor(nazwa)
        data = extract_features(single_file_path)
        features.append([data, class_label])
    # Convert into a Panda dataframe
    featuresdf = pd.DataFrame(features, columns=['feature', 'class_label'])
    print('Finished feature extraction from ', len(featuresdf), ' files')

# Convert features and corresponding classification labels into numpy arrays
X = np.array(featuresdf.feature.tolist())
y = np.array(featuresdf.class_label.tolist())
print("labelsy: ")
print(y)

# Encode the classification labels
le = LabelEncoder()
y = to_categorical(le.fit_transform(y))

# split the dataset
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 42)


num_rows = 40
num_columns = 87
num_channels = 1
print(' xtrain.shape: ', x_train.shape)

x_train = x_train.reshape(x_train.shape[0], num_rows, num_columns, num_channels)
x_test = x_test.reshape(x_test.shape[0], num_rows, num_columns, num_channels)


num_labels = y.shape[1]
print(num_labels)
filter_size = 2

# Construct model
model = Sequential()

model.add(Conv2D(filters=16, kernel_size=2, input_shape=(num_rows, num_columns, num_channels), activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.1))

model.add(Conv2D(filters=32, kernel_size=2, activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.1))

model.add(Conv2D(filters=64, kernel_size=2, activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.1))

model.add(Conv2D(filters=128, kernel_size=2, activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.1))
model.add(GlobalAveragePooling2D())

model.add(Dense(num_labels, activation='softmax'))


# Compile the model
model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

# Display model architecture summary
model.summary()
print("tutaj dobrze")

# Calculate pre-training accuracy
score = model.evaluate(x_test, y_test, verbose=1)
accuracy = 100*score[1]

print("Pre-training accuracy: %.4f%%" % accuracy)


num_epochs = 120
num_batch_size = 16

checkpointer = ModelCheckpoint(filepath='weights_best_cnn.hdf5',
                               verbose=1, save_best_only=True)
start = datetime.now()

model.fit(x_train, y_train, batch_size=num_batch_size, epochs=num_epochs, validation_data=(x_test, y_test), callbacks=[checkpointer], verbose=1)

duration = datetime.now() - start
print("Training completed in time: ", duration)
print("koniec")