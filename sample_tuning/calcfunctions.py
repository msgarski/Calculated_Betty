#!/usr/bin python3.6
import numpy as np
from statistics import mean
import scipy.io.wavfile as sc#import read, write
import pyaudio
import time
import wave
import math
import os

# Ogólne dane pliku audio:
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 3
back_sight = 14


def time_to_frames(num_secs, frame_rate):
    return int(frame_rate * num_secs)
# Gotowa:
def truncate_from(ys, n):
    """Trims a wave array to the given length.
    ys: wave array
    n: integer length
    returns: wave array
    """
    return ys[n:]
# Gotowa:
def truncate_to(ys, n):
    """Trims a wave array to the given length.
    ys: wave array
    n: integer length
    returns: wave array
    """
    return ys[:n]

def truncate_from_to(ys, start=0, end=0):
    """Trims a wave array to the given length.
    ys: wave array
    n: integer length
    returns: wave array
    """
    if(start == 0):
        return ys[:end]
    elif(end == 0):
        return ys[start:]
    else:
        return ys[start:end]

# Gotowa;
def word_from_to(ys, noise_level = 0, block = 4):     # niegotowa
    """
    Function for recognizing where vioce is started
    :param ys: numpy array
    :param threshold:   noise level
    :param block:   size of block
    :return:    frame from which is voice, till which should be cutted
    """
    max_block = int(len(ys) / block)
    num_block = 0
    frame = []
    vals = []
    j = 0
    start_point = 0
    end_point = 0
    while num_block < max_block:
        for i in range(0, block):
            frame.append(math.fabs(ys[j + i]))                      # upload data from j block

        zs = np.array(frame)
        rms2 = (np.sqrt(int(np.mean(zs ** 2))))                     # counting rms from block data
        vals.append(rms2)
        if (num_block > 10) and (start_point == 0):      # szansa na oznaczenie startu
            #print("valx block: ", num_block, "  ", vals[num_block])
            if (vals[num_block] > noise_level)and (vals[num_block - 2] > noise_level) and (vals[num_block - 4] > noise_level):
                #print("jest!!!!")
                start_point = (num_block - 4) * block
                #return start_point
        elif(start_point != 0) and (num_block >= back_sight):    # end point setting
            small_list = vals[num_block-back_sight:num_block]   # todo maybe better to tie with samples numbers
            if (mean(small_list) <= noise_level):#(vals[num_block - 5] < noise_level)and(vals[num_block - 4] < noise_level)and(vals[num_block - 3] < noise_level)and(vals[num_block - 2] < noise_level)and(vals[num_block - 1] < noise_level):
                #print("rozmiar ciszy: ", len(small_list))
                end_point = num_block * block

        if(start_point != 0) and (end_point != 0):
            longitude = end_point - start_point
            if(longitude <= time_to_frames(0.3, 44100)) and (end_point <= 15000):
                ys = truncate_from_to(ys,end_point)
                result2 = word_from_to(ys,noise_level, block)
                return [result2[0], result2[1]]
            else:
                return [start_point, end_point];
        j += block
        num_block += 1
        frame.clear()
    return [start_point, end_point];

# Gotowa:
def threshold(arr, block):
    """
    Function gives us level of threshold counted from
    first 0.5s of file, which is probably only noise...
    :param ys:  numpy array of file fragment
    :param block:   number of frames
    :return:
    """
    max_block = math.floor(len(arr) / block)           # how many blocks of samples is in delivered numpy array
    num_block = 0
    frame = []
    min_max = []                        # todo ale gdzie te wyznaczone 0.5 sekundy trwania???
    j = 0
    while (num_block < max_block):
        for i in range(0, block):
            frame.append(math.fabs(arr[j + i]))         # jump to followed block of array
        j += block
        zs = np.array(frame)
        rms = (np.sqrt(int(np.mean(zs ** 2))))          # counting rms from entire of block
        min_max.append(rms)                             # appending list of rms values of delivered numppy array
        num_block += 1
        #print(num_block, "  ", rms, "  ", len(frame))
        frame.clear()
    #threshold = int(max(min_max) + 1)       # todo a może nie max, ale mean??? z całej array???
    threshold = int(mean(min_max) +1)
    min_max.clear()                         # todo bo może jakiś stuk tam był i teraz zafałszuje nam szum
    return threshold

# Gotowa:
def get_words(word_path):
    with open(word_path) as f:
        flat_list = [word for line in f for word in line.split()]
    return flat_list

def cut_on_start(rec_folder):
    file_list = os.listdir(rec_folder)

def noise_recording(path, rec_folder):
    time.sleep(1)
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    noise_filename = "noise" + ".wav"
    noise_full_path = os.path.join(path, rec_folder, noise_filename)
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    tmp_noise = []  # Array to store sample of ambient noise

    for i in range(0, int(fs / chunk * 0.5)):
        noise_data = stream.read(chunk, exception_on_overflow=False)
        tmp_noise.append(noise_data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    print(len(tmp_noise))
    # Save the recorded noise as a WAV file
    wf = wave.open(noise_full_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(tmp_noise))
    wf.close()
    p.terminate()
    tmp_noise.clear()

def words_sample_recording(full_path):
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    wf = wave.open(full_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    # Terminate the PortAudio interface
    p.terminate()
    frames.clear()

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