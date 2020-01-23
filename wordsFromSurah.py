from collections import Counter
import pickle
import time
import pandas as pd

###
# out is a 2-d list where each inner list is a key, # of occurrences pair for each arabic root wordx
#
###

def open_word(key):
    with open('pckl-words/' + str(key) + '.pckl', 'rb') as fp:
        l = pickle.load(fp)
        # print(l)
    return l

def getSurah(surahNumber, ayahStart, ayahEnd, minCount, maxCount):
    count = 0
    for num in range(1, 1665):
        w = open_word(num)
        if (len(w) <= minCount or len(w) > maxCount):
            continue
        wm = w['wordmorphologies']

        w2 = []


        for i in range(0, len(wm)):
            if (int(wm[i].split('(')[1].split(':')[0]) == surahNumber and int(wm[i].split('(')[1].split(':')[1]) >= ayahStart and int(wm[i].split('(')[1].split(':')[1]) < ayahEnd):
                count = count + 1
                # print(count)
                # w2.append(w.iloc[i])
                question = w['arabicWord'][i]
                answer = w['definition'][i]
                tlit = w['pronunciations'][i]
                ayah = ",".join(wm[i].split('(')[1].split(':')[0:2])
                answer = ' '.join(answer.split('\''))
                print('{',
                        'question:'+ '\''+ question +'\''+ ','+
                        'answer:'+ '\''+ answer +'\''+ ','+
                        'pcklId:'+ str(i) + ','+
                        'tlit:'+ '\''+ tlit +'\''+ ',',
                        'num:'+ '\''+ str(len(w)) +'\''+ ',',
                        'ayah:'+ '\''+ ayah +'\''+ ',',
                        '}'+ ',')


                # print('\''+ answer +'\''+',')

if __name__ == '__main__':
    getSurah(1, 0, 8, 0, 100000)
