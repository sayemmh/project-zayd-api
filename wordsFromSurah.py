from collections import Counter
import pickle
import time
import pandas as pd
import ujson
from constants import NUM_SURAHS_IN_QURAN, NUM_ROOT_WORDS_IN_CORPUS, ALL_AYAHS

def open_rootword(id):
    '''
    Open the DataFrame associated with a particular root word. The `id`s
    go from 1 to 1664 representing the 1664 root words in the corpus.

    :param int id: the id of the rootword to open
    :return: DataFrame containing all words in this root words' group
    :rtype: pandas.core.frame.DataFrame
    '''
    with open('pckl-words/' + str(id) + '.pckl', 'rb') as fp:
        l = pickle.load(fp)
    return l


def get_surah(surahNumber, minCount, maxCount):
    '''
    Get words within a surah starting from one ayah to another. Optional -
    get words with a frequency above `minCount` and lower than `maxCount`.

    :param int surahNumber: which surah to get
    :param int minCount: min frequency of a word to return
    :param int maxCount: max frequency of a word to return
    :return:
    :rtype:
    '''
    count = 0
    list_of_jsons = []
    for num in range(1, NUM_ROOT_WORDS_IN_CORPUS + 1):
        w = open_rootword(num)
        if (len(w) <= minCount or len(w) > maxCount):
            continue
        wm = w['wordmorphologies']



        for i in range(0, len(wm)):
            if (int(wm[i].split('(')[1].split(':')[0]) == surahNumber):
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
                                'frequency': str(len(w)),
                                'surah': ayah.split(',')[0],
                                'ayah': ayah.split(',')[1]
                            }

                # print(word_json)

                list_of_jsons.append(word_json)
                # print(len(list_of_jsons))
                # print('\''+ answer +'\''+',')
    return list_of_jsons

def build_jsons_for_all_surahs():
    for i in range(1, 2 + 1):
        data = get_surah(i, 0, ALL_AYAHS)
        with open(str(i) + '.json', 'w') as f:
            ujson.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    # print(get_surah(1, 0, ALL_AYAHS))
    build_jsons_for_all_surahs()
