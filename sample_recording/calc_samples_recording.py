#!/usr/bin python3.6

from calcfunctions import *



# Deklaracja ścieżki do plików:
path = os.getcwd()
rec_folder = "vioce_samples"
name = input("Podaj imię osoby nagrywanej: ")
base_filename = str("_" + name)
word_file = "lista.txt"
folder_path = os.path.join(path, rec_folder)

# tworzenie folderu do przechowywania nagrań:
try:
    if os.path.exists(folder_path) == 0:
        os.mkdir(folder_path, 0o755)
except:
    print(" Error - "
          "can't create folder - ")

# Ngrywanie próbki szumu zastanego:
noise_recording(path, rec_folder)

# Odczytanie pliku ze słowami do nagrania:
word_path = os.path.join(path, word_file)
# stworzenie listy słów do nagrania:
word_list = get_words(word_path)

for nazwa in word_list:
    filename = nazwa + base_filename + ".wav"
    full_path = os.path.join(folder_path, filename)
    print("wciśnij ENTER")
    print("i powiedz: ", nazwa)
    input()
    print('Recording')
    time.sleep(0.2)
    words_sample_recording(full_path)

print('Finished recording')




