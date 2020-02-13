import snowboydecoder
import sys
import signal
import pyttsx3

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

flaga=0
wynik=0

def operacja():
	global flaga
	a=input("Operacja (-, +, *, / ) : ")

	if a == "-":
		flaga=2
	elif a == "+":
		flaga=1
	elif a == "*":
		flaga=3
	elif a == "/":
		flaga=4
	else:
		print("nie znana operacja")
		operacja()
	
def spiewaj(wynik):
	engine = pyttsx3.init() # object creation

	""" RATE"""
	rate = engine.getProperty('rate')   # getting details of current speaking rate
	#print (rate)                        #printing current voice rate
	engine.setProperty('rate', 125)     # setting up new voice rate


	"""VOLUME"""
	volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
	#print (volume)                          #printing current volume level
	engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

	"""VOICE"""
	voices = engine.getProperty('voices')       #getting details of current voice
	for voice in voices:
		#print(voice)
		if voice.languages[0] == b'\x05pl':
			engine.setProperty('voice', voice.id)
			break
	engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
	#engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

	engine.say("Wynik")
	engine.say(wynik)

	#engine.say('My current speaking rate is ' + str(rate))
	engine.runAndWait()
	engine.stop()


def liczba(znak):
	global wynik
	abc = znak
	print("liczba:", abc)

	if flaga == 1:
		wynik=wynik+abc
	elif flaga == 2:
		wynik=wynik-abc
	elif flaga == 3:
		wynik=wynik*abc
	elif flaga == 4:
		wynik=wynik/abc
	elif flaga == 0:
		wynik=abc
	else:
		print("???")
	
	print("wynik:", wynik)
	spiewaj(wynik)
	operacja()



#engine.say("Hello World!")
#engine.say('My current speaking rate is ' + str(rate))



#models = sys.argv[1:]
models = ["baza/jeden.pmdl","baza/dwa.pmdl", "baza/trzy.pmdl", "baza/cztery.pmdl", "baza/piec.pmdl", "baza/szesc.pmdl", "baza/siedem.pmdl", "baza/osiem.pmdl", "baza/dziewiec.pmdl", "baza/dziesiec.pmdl"]
#models = ["baza/jeden.pmdl","baza/dwa.pmdl", "baza/trzy.pmdl", "baza/cztery.pmdl", "baza/piec.pmdl", "baza/szesc.pmdl", "baza/siedem.pmdl", "baza/osiem.pmdl", "baza/dziewiec.pmdl", "baza/dziesiec.pmdl", "baza/odjac.pmdl", "baza/dodac.pmdl", "baza/pomnozyc.pmdl", "baza/podzielic.pmdl"]

signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]*len(models)
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
callbacks = [lambda: liczba(1), lambda: liczba(2), lambda: liczba(3), lambda: liczba(4), lambda: liczba(5), lambda: liczba(6), lambda: liczba(7), lambda: liczba(8), lambda: liczba(9), lambda: liczba(10)]
#callbacks = [lambda: liczba(1), lambda: liczba(2), lambda: liczba(3), lambda: liczba(4), lambda: liczba(5), lambda: liczba(6), lambda: liczba(7), lambda: liczba(8), lambda: liczba(9), lambda: liczba(10), lambda: odjac(), lambda: dodac(), lambda: pomnozyc(), lambda: podzielic()]


# main loop
# make sure you have the same numbers of callbacks and models
detector.start(detected_callback=callbacks,

               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()



