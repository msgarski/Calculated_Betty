# Program syntetyzuje mowę metodą konkatenacyjną. 
# Do poprawnego działania programu wymagana jest jedynie biblioteka simpleaudio. Prbóbki głosu muszą znajdować się w tym samym folderze co program.
# Syntezator obsługuje liczby rzeczywiste od 0 do 999999,999.
# Funckja recognize() odpowiada za przekształcenie części stałej liczby. Funckja recognizePoint() za część przecinkową.
# Funkcja sayNumber() odczytuje liczbę znajdującą się w zmiennej arrNumber poprzez odtworzenie kolejnych nagrań głosu.

import simpleaudio as sa

arrNumber = []

def say(fl):
    filename = fl
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def sayNumber():
    for i in range(0, len(arrNumber)):
        say(arrNumber[i])

def recognize(number):
    arrNumber.clear()
    number = str(number)
    for i in range(0, len(number)):
        mod = 10**(i+1)
        num = int(number)%mod - sum(arrNumber)
        arrNumber.append(num)
    arrNumber.reverse()
    teens()
    k(number)
    norm()
    return arrNumber

def teens():
    if arrNumber[len(arrNumber) - 2] == 10:
        arrNumber[len(arrNumber) - 2] += arrNumber[len(arrNumber) - 1]
        arrNumber[len(arrNumber) - 1] = 0

def k(number):
    number = int(number)
    if number > 1999 and number < 10000:
        arrNumber[0] = int(arrNumber[0] / 10**3)
        if arrNumber[0] < 5:
            arrNumber.insert(1, '0e')
        else:
            arrNumber.insert(1, '0y')
    
    if number > 9999 and number < 100000:
        arrNumber[0] = int(arrNumber[0] / 10**3)
        arrNumber[1] = int(arrNumber[1] / 10**3)

        if arrNumber[0] == 10:
            arrNumber[0] += arrNumber[1]
            arrNumber[1] = 0

        if arrNumber[0] < 20:
            arrNumber.insert(2, '0y')
        else:
            if arrNumber[1] < 5 and arrNumber[1] > 1:
                arrNumber.insert(2, '0e')
            else:
                arrNumber.insert(2, '0y')
    
    if number > 99999:
        arrNumber[0] = int(arrNumber[0] / 10**3)
        arrNumber[1] = int(arrNumber[1] / 10**3)
        arrNumber[2] = int(arrNumber[2] / 10**3)

        if arrNumber[1] == 10:
            arrNumber[1] += arrNumber[2]
            arrNumber[2] = 0

        if arrNumber[1] < 20:
            arrNumber.insert(3, '0y')
        else:
            if arrNumber[2] < 5 and arrNumber[2] > 1:
                arrNumber.insert(3, '0e')
            else:
                arrNumber.insert(3, '0y')
    
def norm():

    for i in range(0, len(arrNumber)):
        try:
            arrNumber.remove(0)
        except:
            pass

    for i in range(0, len(arrNumber)):
        arrNumber[i] = str(arrNumber[i]) + ".wav"

def convert(inputStr):

    if inputStr.find(","):
        inputStr = inputStr.replace(",", ".")
    return inputStr


def split(inputStr):

    return inputStr.split(".")

def recognizePoint(point):

    arrPoint = []
    arrPoint.append("i.wav")

    if len(point) == 1:
        point = int(point)
        if point == 1:
            arrPoint.append("1a.wav")
        elif point == 2:
            arrPoint.append("2e.wav")
        else:
            arrPoint.append(str(point) + ".wav")

        if point == 1:
            arrPoint.append("10a.wav")
        elif point > 1 and point < 5:
            arrPoint.append("10e.wav")
        else:
            arrPoint.append("10h.wav")
    elif len(point) == 2:
        point = int(point)
        if point < 20:
            if point == 1:
                arrPoint.append("1a.wav")
            elif point == 2:
                arrPoint.append("2e.wav")
            else:
                arrPoint.append(str(point) + ".wav")

            if point == 1:
                arrPoint.append("100a.wav")
            elif point > 1 and point < 5:
                arrPoint.append("100e.wav")
            else:
                arrPoint.append("100h.wav")
        else:
            temp = []
            temp.append(point%10)
            temp.append(point%100 - sum(temp))
            temp.reverse()

            arrPoint.append(str(temp[0]) + ".wav")

            if temp[1] == 2:
                arrPoint.append("2e.wav")
            else:
                arrPoint.append(str(temp[1]) + ".wav")
            
            if temp[1] > 1 and temp[1] < 5:
                arrPoint.append("100e.wav")
            else:
                arrPoint.append("100h.wav")
    else:
        temp = []
        tmp = str(point[1]) + str(point[2])
        tmp = int(tmp)
        h = int(str(point[0]))
        point = int(point)
        if tmp < 20:
            
            if h != 0:
                arrPoint.append(str(h) + "00" + ".wav")

            if point == 1:
                arrPoint.append("1a.wav")
            elif point == 2:
                arrPoint.append("2e.wav")
            else:
                arrPoint.append(str(tmp) + ".wav")

            if point == 1:
                arrPoint.append("1000a.wav")
            elif point > 1 and point < 5:
                arrPoint.append("1000e.wav")
            else:
                arrPoint.append("1000h.wav")
        else:
            
            temp.append(point%10)
            temp.append(point%100 - sum(temp))
            temp.append(point%1000 - sum(temp))
            temp.reverse()

            if temp[0] != 0:
                arrPoint.append(str(temp[0]) + ".wav")
            arrPoint.append(str(temp[1]) + ".wav")

            if temp[2] == 2:
                arrPoint.append("2e.wav")
            else:
                arrPoint.append(str(temp[2]) + ".wav")
            
            if temp[2] > 1 and temp[2] < 5:
                arrPoint.append("1000e.wav")
            else:
                arrPoint.append("1000h.wav")

    return arrPoint


#Main

while(1):

    a = convert(input("Podaj liczbe: "))
    if float(a) < 1000000:

        a = split(str(round(float(a), 3)))
        integ = a[0]
        point = a[1]
        
        recognize(integ)
        if int(point) > 0:
            arrNumber.extend(recognizePoint(point))
        print(arrNumber)
        sayNumber()
        

    else: 
        print("Podaj liczbe mniejsza niz 1.000.000")
