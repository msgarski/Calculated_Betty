import speech_recognition as s_r
print(s_r.__version__)

r = s_r.Recognizer()
print(s_r.Microphone.list_microphone_names()) # print all the microphones connected to your machine
my_mic = s_r.Microphone(device_index=1)     # ? czy na pewno ten numer?

with my_mic as source:
    print("Say now!!!!")
    r.adjust_for_ambient_noise(source, duration=0.5)  # przez 0.5 sek ustala poziom szumu "własnego"
    nagranie = r.listen(source)
#print(r.recognize_google(nagranie))