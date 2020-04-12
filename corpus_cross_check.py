from bs4 import BeautifulSoup
import requests
import pandas as pd 
import ujson
import json
import urllib
from constants import NUM_SURAHS_IN_QURAN, NUM_ROOT_WORDS_IN_CORPUS, ALL_AYAHS

def getPageContent(hyperlink):
    page_response = requests.get(hyperlink, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    return page_content

def getAyahNum(wordRow):
    return wordRow.find_all("td")[0].find("span").text.split(":")[1]
def getWordNum(wordRow):
    return wordRow.find_all("td")[0].find("span").text.split(":")[2].split(")")[0]

def checkWord(surahNum, ayahNum, wordNum, all_rootwords_in_surah):
	wordFound = False
	for rootword_in_surah in all_rootwords_in_surah:
		rootAyahNum = int(rootword_in_surah['ayahnum'])
		rootWordNum = int(rootword_in_surah['wordnum'])
		if (ayahNum == rootAyahNum) and (wordNum == rootWordNum):
			wordFound = True
	if not wordFound:
		hyperlink = 'http://corpus.quran.com/wordbyword.jsp?chapter=' + str(surahNum) + '&verse=' + str(ayahNum)
		page_content = getPageContent(hyperlink)
		wordTable = page_content.find_all("table",{"class":"morphologyTable"})[0]
		wordRows = wordTable.find_all("tr", {"class": None})

		for wordRow in wordRows:
			if (getWordNum(wordRow) == str(wordNum)) and (getAyahNum(wordRow) == str(ayahNum)):
				tlit = wordRow.find_all("td")[0].find("span", {"class":"phonetic"}).text
				translation = str(wordRow.find_all("td")[0]).split("<br/>")[2].split("<")[0].strip().strip(",").strip(".")
				print(str(surahNum) + ':' + str(ayahNum) + ':' + str(wordNum))
				print(tlit)
				print(translation)
				return tlit, translation


def build_jsons_for_leftovers():

	with open("all_words_morphemes.json", 'r') as f:
		json_data = f.read()
	all_words_in_quran = json.loads(json_data)
	list_of_jsons = []
	for count, word in enumerate(all_words_in_quran):
		surahNum = word['surahnum']
		ayahNum = word['ayahnum']
		wordNum = word['wordnum']

		if (surahNum <14):

			continue

		with open('json-surah-words/' + str(surahNum) + '.json' , 'r' ) as f:
			rootwords_in_surah = f.read()
		all_rootwords_in_surah = json.loads(rootwords_in_surah)
	
		result = checkWord(surahNum, ayahNum, wordNum, all_rootwords_in_surah)
		if result is not None:
			word_json = {
	                        'surahnum': surahNum,
	                        'ayahnum': ayahNum,
	                        'wordnum': wordNum,
	                        'answer' : result[1],
	                        'tlit' : result[0]
						}
			print(word_json)
			list_of_jsons.append(word_json)
	
		if (count % 100) == 0:
			with open('cross_check_words_3.json','w') as f:
				ujson.dump(list_of_jsons,f,ensure_ascii=False, indent=4)
				f.close()	
if __name__ == '__main__':
    build_jsons_for_leftovers()
