import pandas as pd
import ujson
import json
import constants


def get_surah(surah_number, surah_df, difficulty_map):
    list_of_jsons = list()
    ayah_count = surah_df['ayahnum'].max()

    for i in range(1, ayah_count + 1):
        result_df = surah_df.loc[surah_df['ayahnum'] == i]
        id_list = list()
        difficulty = 0
        for ind in result_df.index:
            id_list.append((result_df['rootWordId'][ind].item(), result_df['waznType'][ind]))
            difficulty += difficulty_map.get((result_df['rootWordId'][ind], result_df['waznType'][ind]))
        if len(id_list) > 0:
            difficulty /= pow(len(id_list),2)
        json_ayah = {'Ayah': i, 'Surah': surah_number,
                     'word_ids': id_list, 'Difficulty': difficulty}
        list_of_jsons.append(json_ayah)

    return list_of_jsons


def build_jsons_for_all_surahs():
    prefix = 'json-surah-words/'
    difficulty_map = build_map()
    for i in range(1, constants.NUM_SURAHS_IN_QURAN + 1):
        surah_df = pd.read_json(prefix + str(i) + '.json')
        data = get_surah(i, surah_df, difficulty_map)
        with open('ayahRoots/' + str(i) + '.json', 'w') as f:
            ujson.dump(data, f, ensure_ascii=False, indent=4)
            f.close()


def build_map():
    with open('word-statisics.json') as f:
        data = json.load(f)
    df = pd.read_json(data)
    result_map = dict()
    for ind in df.index:
        rootId = df['rootWordId'][ind]
        part_of_speech = df['partOfSpeech'][ind] 
        score = ((df['timesAppeared'][ind] * 3 + (df['commonAyahs'][ind] * 5))
             * df['frequencyInAyah'][ind])/ (df['ayahBias'][ind]) # score for each word, bias towards common ayahs and times appeared
        result_map[(rootId, part_of_speech)] = score * 100
    
    with open('word-scores.json', 'w') as f:
        ujson.dump(result_map, f, indent=4)
        f.close()

    return result_map

def build_word_map():
    prefix = 'json-surah-words/'
    word_df = pd.DataFrame(columns=['rootWord','rootWordId','Definition','partOfSpeech','timesAppeared','ayahsAppeared','frequencyInAyah',
    'ayahBias', 'commonAyahs'])
    constantBias = 3
    commonSurahList = [str(x) for x in range(94,115)]
    commonSurahList.extend(('1', '36', '55')) # fatiha, yaseen, rahman
    commonAyahList = ['18:1','18:2','18:3','18:4','18:5','18:6','18:7','18:8','18:9',
                      '18:10','2:255'] # first ten ayats of kahf and ayat ul kursi
    for i in range(1, 115):
        surah_df = pd.read_json(prefix + str(i) + '.json')
        
        for ind in surah_df.index:
            ayah = [surah_df['surahnum'][ind].astype(str) + ':' + surah_df['ayahnum'][ind].astype(str)] # ayah as [surah num: verse num] -> ['1:2']
            ayah_df = surah_df.loc[surah_df['ayahnum'] == surah_df['ayahnum'][ind]] # get all words belonging to that ayah
            word_in_ayah = ayah_df.loc[ayah_df['rootWordId'] == surah_df['rootWordId'][ind]]
            common = 0
            if ayah[0] in commonAyahList or surah_df['surahnum'][ind].astype(str) in commonSurahList:
                common = 1
            if surah_df['rootWordId'][ind] in word_df.rootWordId.values:
                row = word_df.loc[(word_df['rootWordId'] == surah_df['rootWordId'][ind]) & (surah_df['waznType'][ind] == word_df['partOfSpeech'])] 
                # word with same part of speech already exists
                if row.size > 0:
                    row['timesAppeared'] += 1
                    row['commonAyahs'] += common
                    if ayah[0] not in row.iloc[0,3]:
                        row.ayahsAppeared = row.ayahsAppeared.apply(lambda x: x+ayah)
                    else:
                        ayah_frequency = word_in_ayah.size / ayah_df.size
                        frequency = (ayah_frequency + row['frequencyInAyah']) / row['ayahsAppeared'].str.len()
                        bias = (constantBias * ayah_df.size) + frequency
                        row['frequencyInAyah'] = frequency
                        row['ayahBias'] = bias

                    word_df.loc[(word_df['rootWordId'] == surah_df['rootWordId'][ind]) & (surah_df['waznType'][ind] == word_df['partOfSpeech'])] = row
                else:
                    word_df = create_row(word_in_ayah, ayah_df, constantBias, word_df, surah_df, common, ind, ayah) # new entry to dataframe

            else:
                word_df = create_row(word_in_ayah, ayah_df, constantBias, word_df, surah_df, common, ind, ayah)

    with open ('word-statistics.json', 'w') as f:
        ujson.dump(word_df.to_json(orient='records',force_ascii=False), f, ensure_ascii=False, indent=4)
        f.close()
    build_jsons_for_all_surahs()

def create_row(word_in_ayah, ayah_df, constantBias, word_df, surah_df, common, ind, ayah):
    frequency = word_in_ayah.size / ayah_df.size
    bias = (constantBias * ayah_df.size) + frequency
    word_df = word_df.append({'rootWord': surah_df['rootWord'][ind], 'rootWordId':
                            surah_df['rootWordId'][ind], 'Definition': surah_df['waznEnglish'][ind],
                            'partOfSpeech': surah_df['waznType'][ind],
                            'timesAppeared': 1, 'ayahsAppeared': list(ayah),
                            'frequencyInAyah': frequency, 'ayahBias': bias, 
                            'commonAyahs': common}, ignore_index=True)
    return word_df

if __name__ == '__main__':
    build_word_map()