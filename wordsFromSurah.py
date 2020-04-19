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
    answers = []
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
                rootWord = w['rootWord'][i]
                rootWordType = w['rootWordType'][i]
                wordForms = w['wordForms'][i]
                wordFormDefs = w['wordFormDefs'][i]
                wordFormTlits = w['wordFormTlits'][i]
                wordFormTypes = w['wordFormTypes'][i]
                arabicAyah = w['arabicAyah'][i]

                ayah = ",".join(wm[i].split('(')[1].split(')')[0].split(':')[0:3])
                answer = ' '.join(answer.split('\''))

                word_json = {
                                'question': question,
                                'answer': answer,
                                'pcklId': str(i),
                                'rootWordId': num,
                                'tlit': tlit,
                                'frequency': str(len(w)),
                                'surahnum': ayah.split(',')[0],
                                'ayahnum': ayah.split(',')[1],
                                'wordnum': ayah.split(',')[2],
                                'arabicAyah' : arabicAyah,
                                'rootWord': rootWord,
                                'rootWordType':rootWordType,
                                'wazn': wordForms,
                                'waznEnglish' : wordFormDefs,
                                'waznTlit' : wordFormTlits,
                                'waznType' : wordFormTypes
                            }

                answers.append(answer)

                list_of_jsons.append(word_json)
                # print(len(list_of_jsons))
                # print('\''+ answer +'\''+',')
    answers = list(set(answers))
    return list_of_jsons, answers

def build_jsons_for_all_surahs():
    for i in range(1, NUM_SURAHS_IN_QURAN + 1):
        print("Building for surah: " + str(i))
        data, answers = get_surah(i, 0, ALL_AYAHS)
        print(data)
        print("Num words in surah: " + str(len(data)))
        print(answers)
        with open('json-surah-words/' + str(i) + '.json', 'w') as f:
            f.write("var words = \n")
            ujson.dump(data, f, ensure_ascii=False, indent=4)
            f.write("; \n")
            f.write("export default words;")
            f.close()

        with open('json-surah-words/' + str(i) + '_answers' + '.json', 'w') as f:
            f.write("var answers = \n")
            ujson.dump(answers, f)
            f.write("; \n")
            f.write("export default answers;")
            f.close()

        # input()    
if __name__ == '__main__':
    # print(get_surah(1, 0, ALL_AYAHS))
    build_jsons_for_all_surahs()
