import  audiomonitor as am
import time


s = am.Audiomonitor()
s.base_filename = "_A_name"
s.rec_folder = "nagrania"
s.recording()
time.sleep(30)      # program will work for 30 sec
s.stop_recording()

