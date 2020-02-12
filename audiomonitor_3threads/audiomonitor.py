#!/usr/bin python3

import pyaudio
import numpy as np
import threading
import queue
import math
import struct
from scipy.io.wavfile import write
import time
import os
"""

        This file is undependent from other scripts

"""
class Audiomonitor():
    directory = os.getcwd()
    rec_folder = "nagrania"
    path = os.path.join(directory, rec_folder)
    base_filename = "_t_word"

    def __init__(self):
        self.block = 1024                                        # size of buffer(in number of samples)
        self.format = pyaudio.paInt16                           # bit's deep per sample 16 bits
        self.channels = 1                                       # mono or stereo
        self.frame_rate = 44100                                 # Record at 44100 samples per second
        self.finish_flag = False                                # flag for closing threads
        self.gap_size = 0.06                                  # longitude of inside word break
        self.noise_multiplier = 1.5                             # for adjusting counted noise level
        self.shortest_word = 0.15                                # how long takes the shortest word?

    def recording(self):
        try:
            self.p = pyaudio.PyAudio()                                  # Create an interface to PortAudio
            self.in_data_queue = queue.Queue()
            self.out_data_queue = queue.Queue()
            self.terminate_queue = queue.Queue()
        except:
            print("Błąd przy pyaudio i kolejkach... f-cja recording...")

        print("Noise Recording........")
        try:
            self.noise_level = self.noise_multiplier * self.noise_levels()
            # self.noise_level = 100                                       # to tylko gdy funkcja nie działała
            print('Poziom szumu = ', self.noise_level)
        except:
            print("Błąd przy oznaczeniu szumu... f-cja recording...")

        time.sleep(1)
        try:
            self.t_rec = threading.Thread(target=self.record_audio)
            self.t_signal_process = threading.Thread(target=self.word_creating)
            self.t_saving = threading.Thread(target=self.save_words_from_queue)
        except:
            print("Błąd przy tworzeniu wątków... f-cja recording...")

        print("Recording........")
        try:                                                                 # Start threads:
            self.t_rec.start()
            self.t_signal_process.start()
            self.t_saving.start()
        except:
            print("Startowanie wątków nieudane!!!!!  - funkcja preparation")

    def stop_recording(self):
        try:
            self.finish_flag = True
            self.t_rec.join()
            self.t_signal_process.join()
            self.t_saving.join()
            self.p.terminate()
            print("KONIEC")
        except:
            print("Błąd w f-cji stop_recording...")
            print("zamknięcie wątków nieudane...")

    def record_audio(self):
        try:
            self.istream = self.p.open(format=self.format,              # opening of stream
                             channels=self.channels,
                             rate=self.frame_rate,
                             input=True,
                             frames_per_buffer=self.block)
        except:
            print("Błąd otwarcia strumienia - f-cja: record_audio...")

        #i = 0                   # po co to i ?                          #todo może to usunąć?
        while self.finish_flag == False:                                # todo ustalić ile ma trwać nagrywanie do bufora - wiecznie?
            try:                                                        # when the pyaudio object is destroyed, stops
                data_str = self.istream.read(self.block,
                                             exception_on_overflow=False)# read a chunk of data
            except:
                print("Błąd pobrania danych ze strumienia  -  f-cja: record_audio...")
                break
            self.in_data_queue.put( data_str)                           # append chunk to queue
            #i +=1
        self.in_data_queue.put(None)                                    # todo tutaj możena dać stream.close....
        self.istream.close()
        print("Nagrane, więc kończę.... zamykam wątek...",
              self.in_data_queue.qsize())                               # todo czy to potrzebne?

    def time_to_frames(self, num_secs):
        return int(self.frame_rate * num_secs)

    def get_rms(self,chunk):
        """
        Function  for counting rms level from byte-like data chunk
        RMS amplitude is defined as the square root of
        the mean over time of the square of the amplitude,
        so we need to convert this string of bytes into a string of 16-bit samples...
        """
        count = len(chunk)/2
        format = "%dh"%(count)
        shorts = struct.unpack( format, chunk )
        sum_squares = 0.0
        for sample in shorts:
            n = sample  # * (1.0/32768.0)
            sum_squares += n*n
        return math.sqrt( int(sum_squares / count) )

    def noise_levels(self):
        """
        Function for recording noise sample and counting level of ambient noise
        :return:        level of ambient noise
        """
        check_time = 0.5                                                   # noise sample recording time in seconds
        self.stream = self.p.open(format=self.format,
                        channels=self.channels,
                        rate=self.frame_rate,
                        frames_per_buffer=self.block,
                        input=True)

        fr = []                                                     # Initialize array to store frames
        for i in range(0,int(self.frame_rate/self.block * check_time)):# Store data in chunks until n seconds
            data = self.stream.read(self.block, exception_on_overflow=False)
            fr.append(data)
        sum =0
        for i in range(0, len(fr)):
            noise = self.get_rms(fr[i])
            sum += noise
        mean_noise = sum/len(fr)
        self.stream.stop_stream()                                        # Stop and close the stream
        self.stream.close()
        return mean_noise

    def word_creating(self):
        """
        This function gets recorded chunks of audio and
        recognize where voice starts
        recognize where voice stops
        and records these word to out_queue for additional process...
        """
        start_point = False
        gap = self.time_to_frames(self.gap_size)                     # how long could be break inside a word np 0.08
        print("Please, speak...gap is: ", gap)                           # todo mam też zmienną gap_size jako czas przerwy
        i = 0
        j = 0
        try:
            while True:
                i += 1
                try:
                    x = self.in_data_queue.get()
                    if x is None:
                        break
                except:
                    print("Błąd pobrania danych do obróbki  -  f-cja: word_creating...")

                fra = np.fromstring(x, dtype=np.int16, count=-1)
                rms = self.get_rms(x)
                if (start_point == False):
                    if rms > self.noise_level:                          # start of word...
                        start_point = True
                        word = np.copy(fra)
                else:
                    if rms > self.noise_level:
                        j = 0
                        word = np.concatenate((word, fra))
                    else:
                        j += self.block
                        if (j > gap):
                            j = 0
                            if len(word) > self.time_to_frames(self.shortest_word):
                                self.out_data_queue.put(word)           # Puting entire word into out_queue
                                start_point = False
                            else:                                       # word is too short to be a real word
                                start_point = False
                        else:
                            word = np.concatenate((word, fra))
        except:
            print("Błąd w pętli while  -  f-cja: word_creating...")

        print("Wychodzę z tworzenia słów, bo to koniec... zamykam wątek")
        self.out_data_queue.put(None)

    def save_words_from_queue(self):
        """
        Function which records wav file from queue data (numpy arrays),
        which are extracted voice files
        whith one separate word per one file
        """
        index = 0                                                   # index of word - part of the filename
        try:
            while True:
                index += 1
                data = self.out_data_queue.get()
                if data is None:
                    break
                try:
                    if os.path.exists(self.path) == 0:
                        os.mkdir(self.path, 0o755)
                except:
                    print(" Error - "
                          "can't create folder - "
                          "function: save_words_from_queue...")

                filename = str(index)+self.base_filename+'.wav'
                full_file_path = os.path.join(self.path, filename)
                write(full_file_path, self.frame_rate, data)
                print("--------------SŁOWO DODANE------------")
        except:
            print(" Error in while loop - function: save_words_from_queue...")

        print("Konczę zapisywanie słów z nagrania...zamykam się...wątek")    #todo do późniejszego usunięcia


"""
# lines below are useable for checking if all methods within class are working properly:
s = Audiomonitor()
s.base_filename = "_A_name"
s.rec_folder = "nagrania"
s.recording()
time.sleep(20)
s.stop_recording()
exit()
"""







