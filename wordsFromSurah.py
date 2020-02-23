from collections import Counter
import pickle
import time
import pandas as pd
import ujson

'''
Open the DataFrame associated with a particular root word. The `id`s
go from 1 to 1664 representing the 1664 root words in the corpus.

:param int id: the id of the rootword to open
:return: DataFrame containing all words in this root words' group
:rtype: pandas.core.frame.DataFrame
'''
def open_rootword(id):

    with open('pckl-words/' + str(id) + '.pckl', 'rb') as fp:
        l = pickle.load(fp)
    return l


'''
Get words within a surah starting from one ayah to another. Optional -
get words with a frequency above `minCount` and lower than `maxCount`.

:param int surahNumber: which surah to get
:param int ayahStart: which ayah to start at
:param int ayahEnd: which ayah to end at
:param int minCount: min frequency of a word to return
:param int maxCount: max frequency of a word to return
:return:
:rtype:
'''
def getSurah(surahNumber, ayahStart, ayahEnd, minCount, maxCount):
    ayahStart += 1
    ayahEnd += 1
    count = 0
    list_of_jsons = []
    for num in range(1, 1665):
        w = open_rootword(num)
        if (len(w) <= minCount or len(w) > maxCount):
            continue
        wm = w['wordmorphologies']



        for i in range(0, len(wm)):
            if (int(wm[i].split('(')[1].split(':')[0]) == surahNumber and int(wm[i].split('(')[1].split(':')[1]) >= ayahStart and int(wm[i].split('(')[1].split(':')[1]) < ayahEnd):
                print("hi")
                count = count + 1
                # print(count)
                # w2.append(w.iloc[i])
                question = w['arabicWord'][i]
                answer = w['definition'][i]
                tlit = w['pronunciations'][i]
                ayah = ",".join(wm[i].split('(')[1].split(':')[0:2])
                answer = ' '.join(answer.split('\''))
                # print('{',
                #         'question:'+ '\''+ question +'\''+ ','+
                #         'answer:'+ '\''+ answer +'\''+ ','+
                #         'pcklId:'+ str(i) + ','+
                #         'tlit:'+ '\''+ tlit +'\''+ ',',
                #         'num:'+ '\''+ str(len(w)) +'\''+ ',',
                #         'ayah:'+ '\''+ ayah +'\''+ ',',
                #         '}'+ ',')
                word_json = {
                                'question': question,
                                'answer': answer,
                                'pcklId': str(i),
                                'tlit': tlit,
                                'num': str(len(w)),
                                'ayah': ayah
                            }

                # print(word_json)

                list_of_jsons.append(word_json)
                print(len(list_of_jsons))
                # print('\''+ answer +'\''+',')
    return ujson.dumps(list_of_jsons)


if __name__ == '__main__':
    a = getSurah(1, 1, 7, 0, 100000)
    print(a)
