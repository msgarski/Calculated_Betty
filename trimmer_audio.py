from scipy.io.wavfile import read, write
import numpy as np
import os
from calcfunctions import *

path = os.getcwd()                                          # getting path to recent folder
samp_folder = "nagrania"
save_folder = "nagrania/records_calculator"                 #todo Path to audio files  - I need to change it
path_samp = os.path.join(path, samp_folder)
path_save = os.path.join(path, save_folder)
frame_rate = 44100
block = 512
noise_level = 30
                                                                    # function for get first part of filename
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

try:
    file_list = os.listdir(path_samp)                       # getting list of files from declared path with samples
except:
    print("nie otwiera folderu????")

for nazwa in file_list:                                     # todo policzyć jeszcze noise level
    abs_path = os.path.join(path_samp, nazwa)               # exact absolute path to file from list
    if os.path.isfile(abs_path):                            # if element of list is real file...do something:
        a = read(abs_path)
        data = np.array(a[1],dtype=np.int16)                # changing opened file to numpy array
        dist = time_to_frames(0.3, frame_rate)
        noise_sample = truncate_to(data,dist)               # truncate part of array for noise level measuring
        noise_level = threshold(noise_sample, block)        # noise level measuring
        result = word_from_to(data,noise_level, block)      # recognizing, where is word
        word = truncate_from_to(data,result[0],result[1])
        #word = truncate_from(data, result[0])
        word_size = len(word)

        try:                                                 # reports printing
            if (result[0] == 0) or (result[1] == 0):
                try:                                         # -> this is not good effect...save it!!!
                    cutted_word = open("report_cut_word.txt", "a")
                except:
                    print("Nieudane otwarcie pliku report_cut_word.txt!!!")
                cutted_word.write(nazwa + '\n')
                cutted_word.close()
        except:
            print("Nieudany zapis do pliku tekstowego: report_cut_word.txt!!!")

        try:
            if word_size < time_to_frames(0.3, frame_rate):  # if word is shorter than 0.5 sec ->
                try:                                         # -> this is not good effect...save it!!!
                    report_file = open("raport_err.txt", "a")
                except:
                    print("Nieudane otwarcie pliku txt!!!")
                report_file.write(nazwa + '\n')
                report_file.close()
        except:
            print("Nieudany zapis do pliku tekstowego!!!")
        name_of_class = classname_extractor(nazwa)
        print("nazwa: ", nazwa, "rozmiar: ", word_size, "start i end: ",
              result, " nazwa klasy: ", name_of_class)
        filename = os.path.join(path_save, nazwa)           # new path for cutted words
        write(filename, frame_rate, word)                   # saving "new" word as .wav file


