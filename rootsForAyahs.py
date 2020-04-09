import pandas as pd
import ujson

def get_surah(surah_number, surah_df):
	list_of_jsons = list()
	ayah_count = surah_df['VerseNo'].max()

	for i in range(1, ayah_count + 1):
		result_df = surah_df.loc[surah_df['VerseNo'] == float(i)]
		id_list = list()
		for ind in result_df.index:
			id_list.append(result_df['RootWordId'][ind])
		json_ayah = {'Ayah': i, 'Surah': 1, 'word_ids': id_list}
		list_of_jsons.append(json_ayah)

	return list_of_jsons

def build_jsons_for_all_surahs():
	filename = 'arabic_root_words.csv'
	full_df = pd.read_csv(filename)
    for i in range(1, NUM_SURAHS_IN_QURAN + 1):
        print("Building for surah: " + str(i))
        surah_df = surah_df.loc[surah_df['ChapterNo'] == str(i)]
        data = get_surah(i, surah_df)
        with open(str(i) + '.json', 'w') as f:
            f.write("var words = \n")
            ujson.dump(data, f, ensure_ascii=False, indent=4)
            f.write("; \n")
            f.write("export default words;")


if __name__ == '__main__':
    build_jsons_for_all_surahs()