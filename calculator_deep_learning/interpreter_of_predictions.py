
def last_score(compute):
    if (len(compute) == 0):
        print("Nie ma czego liczyć...")
        return 0
    sum = ''
    for el in compute:
        if(isinstance(el, str)):
            if(el == 'plus') or (el == 'dodac'):
                sum += '+'
            elif(el == 'ray'):
                sum += '*'
            elif(el == 'podzielic') or (el == 'przez'):
                sum += '/'
            elif(el == 'minus') or ( el == 'odjac'):
                sum += '-'
        else:
            sum += str(el)
    return eval(sum)

def evaluate(prediction):
    lb = [                               # indexes:
        0, 1, 10, 3, 1000,                          # 0 .. 4
        11, 12, 13, 14, 15,                         # 5 .. 9
        16, 17, 18, 19, 2,                          # 10 .. 14
        20, 200, 3, 30, 300,                        # 15 - 19
        4, 40, 400, 5, 50,                          # 20 - 24
        500, 6, 60, 600, 7,                         # 25 - 29
        70, 700, 8, 80, 800,                        # 30 - 34
        9, 90, 900, 'dodac', 'koniec',              # 35 - 39
        'minus', 'nn', 'odjac', 'plus', 'podzielic',# 40 - 44
        'brak', 'przez', 'razy', 'stop', 'wynik']   # 45 - 49

    compute = []
    wynik = 0
    while True:
        # pobranie słowa z kolejki

        # predict...

        # uzyskanie max_clas jako indeksu tablicy labelsów

        x = prediction
        if(lb[x] == 'nn') or (lb[x] == 'stoop'):
            continue

        if(len(compute) == 0):                    # list is empty on start
            if(lb[x] == 'minus') or (lb[x] == 'odjac') or ((x <= 37) and (x >= 0)):
                compute.append(lb[x])
                continue
            else:
                if(lb[x] == 'wynik'):
                    print("Nie ma jeszcze czego liczyć...")
                    continue
                elif(lb[x] == 'koniec'):
                    break                          # todo poza pętlą ustawić flagę i zakończyc wątki
        else:                                       # list is not empty
            if((x <= 37) and (x >= 0)):             # x is a number
                if(isinstance(compute[-1], str)):   # in the list is sign, not a number
                    compute.append(lb[x])
                    continue
                else:                       # last element of the list is a number
                    compute[-1] += lb[x]    # so we can add ane number to another
                    continue                # and go to new iteration
            else:                           # x is not a number, is a sign or terminate
                if(isinstance(compute[-1], str)):  # in the list is sign, not a number
                    if (lb[x] == 'wynik'):
                        compute.pop()          # delete sign at the end of the list
                        wynik = last_score(compute)       # todo obsłużyć wynik
                        continue
                    elif (lb[x] == 'koniec'):
                        compute.pop()          # delete sign at the end of the list
                        wynik = last_score(compute)       # todo obsłużyć wynik
                        break               # todo poza pętlą ustawić flagę i zakończyc wątki
                    else:
                        continue
                else:                       # number at the end of the list
                    if (lb[x] == 'wynik'):
                        wynik = last_score(compute)  # todo obsłużyć wynik
                        continue
                    elif (lb[x] == 'koniec'):
                        wynik = last_score(compute)  # todo obsłużyć wynik
                        break  # todo poza pętlą ustawić flagę i zakończyc wątki
                    else:
                        compute.append(lb[x])
                        continue

        # tutaj zrobię ustawienie flagi
    return wynik