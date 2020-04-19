import pandas as pd 
import ujson
import json
import requests
from bs4 import BeautifulSoup

def getPageContent(hyperlink):
    page_response = requests.get(hyperlink, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    return page_content

def get_all_word_defs():
	translation_arr = []
	arabic_arr = []
	english_arr = []
	surahnum_arr = []
	ayahnum_arr = []
	wordnum_arr = []
	base = 'https://quranwbw.com/4'
	page_content = getPageContent(base)
	print(page_content)
	input()
	for surahnum in range(68,69):
		surahLink = base + str(surahnum)
		page_content = getPageContent(surahLink)
		surah = page_content.find("div",{"class":"ayahs rtl"})
		ayahs = surah.find_all("p")
		for ayahnum, ayah in enumerate(ayahs):
			arabic_words = ayah.find_all("span",{"class":"ar quranText top first rtl"})
			english_words = ayah.find_all("span",{"class":"en second ltr"})
			for wordnum, arabic_word in enumerate(arabic_words):
				arabic_arr.append(arabic_word.text)
				ayahnum_arr.append(ayahnum+1)
				wordnum_arr.append(wordnum+1)
				surahnum_arr.append(surahnum)
				print(str(surahnum) + ":" + str(ayahnum+1) + ":" + str(wordnum+1))
			for english_word in english_words:
				english_arr.append(english_word.text)
	print("here")
	df = pd.DataFrame({'arabicWord':arabic_arr})
	df['answer'] = english_arr
	df['surahnum'] = surahnum_arr
	df['ayahnum'] = ayahnum_arr
	df['wordnum'] = wordnum_arr
	return df


	# list_of_jsons = []
	# with open(filename, 'r') as f:
	# 	json_data = f.read()
	# newWords = json.loads(json_data)
	# df = pd.read_json(filename)
	# print(df['tlit'].value_counts())
	# freqDict = df['tlit'].value_counts().to_dict()
	# for newWord in newWords:
	# 	tlit = newWord['tlit']
	# 	newWord.update(frequency= freqDict.get(tlit))
	# 	list_of_jsons.append(newWord)
	# with open("cross_check_words_frequency.json", 'w') as fw:
	# 	ujson.dump(list_of_jsons,fw,ensure_ascii=False, indent=4)
	# 	fw.close()
	


if __name__ == '__main__':
	list_of_jsons = []
	df = pd.read_json("cross_check_words_frequency.json")
	print(df)
	input()
	# for i in range(1,len(df)):
	# 	surah_num = print(type(df['surahnum'][i]))
	# 	ayah_num = df['ayahnum'][i]
	# 	word_num = df['wordnum'][i]
	dfall = get_all_word_defs()
	merged_inner = pd.merge(left = df, right = dfall, left_on=['surahnum','ayahnum','wordnum'], right_on=['surahnum','ayahnum','wordnum'])
	merged_inner.to_json("merged.json")
	for i in merged_inner.index:
		word_json = {
						'question': merged_inner['arabicWord'][i],
						'answer': merged_inner['answer_x'][i],
						'surahnum' : merger_inner['surahnum'][i],
						'ayahnum' : merged_inner['ayahnum'][i],
						'wordnum' : merged_inner['wordnum'][i],
						'frequency': merged_inner['frequency'][i],
						'tlit' : merged_inner['tlit'][i]
					}
		list_of_jsons.append(word_json)

