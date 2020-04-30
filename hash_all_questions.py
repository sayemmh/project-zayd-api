import hashlib
import ast
import ujson
from constants import NUM_SURAHS_IN_QURAN, NUM_ROOT_WORDS_IN_CORPUS, ALL_AYAHS

json_surah_location = 'json-surah-words/'

def add_hash_field_to_questions():
    all_hashes = {}
    count = 1
    for i in range(2, NUM_SURAHS_IN_QURAN + 1):
    # for i in [110]:

        with open(json_surah_location + str(i) + '.json', 'r') as f:
            surah = f.read()
            # print(surah)
            # print(type(surah))
            # input()
            # print(i)
            surah = ast.literal_eval('[' + surah + ']')

        list_of_jsons = []
        for word in surah:
            print(count)
            count += 1

            s = append0s(str(word['surahnum'])) + '_' + append0s(str(word['ayahnum'])) + '_' + append0s(str(word['wordnum']))
            word['surahayahnum'] = s

            h = int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % 10**12
            word['question_id'] = h
            if h not in all_hashes:
                all_hashes[h] = s
            else:
                print(all_hashes[h])
                print(s)
                input("we messed up")
            list_of_jsons.append(word)
        with open('json-surah-words/' + str(i) + '.json', 'w') as f2:
            ujson.dump(list_of_jsons, f2, ensure_ascii=False, indent=4)
            f2.close()

def append0s(number):
    ret = str(number)
    if len(ret) == 1:
        ret = '00' + ret
    elif len(ret) == 2:
        ret = '0' + ret
    return ret

if __name__ == '__main__':
    add_hash_field_to_questions()
