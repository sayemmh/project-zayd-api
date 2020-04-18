from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import ujson
# import json
import pickle

arabic_word_arr = []
ayahnum_arr = []
wordnum_arr = []
surahnum_arr = []


def get_all_words(driver):
	for surahnum in range(1,115):
		driver.get('https://quranwbw.com/' + str(surahnum))
		time.sleep(2)
		lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
		match=False
		while(match==False):
			lastCount = lenOfPage
			time.sleep(0.2)
			lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
			if lastCount==lenOfPage:
				match=True
		html = driver.page_source
		page_content = BeautifulSoup(html, "html.parser")
		ayahtotal = len(page_content.find("div",{"class":"ayahs-block"}).find_all("div",{"class":"row ayah-row"}))
		print(ayahtotal)

		for ayahnum in range(1,ayahtotal+1):
			classtype = "col-10 single-ayah " + str(ayahnum)
			words = page_content.find("div", {"class":classtype}).find_all("span",{"class":"word-arabic"})
			print("extracting for ayah:"+str(ayahnum))
			wordnum = 0
			for word in words:
				wordnum = wordnum + 1
				arabic_word_arr.append(word.text)
				surahnum_arr.append(surahnum)
				ayahnum_arr.append(ayahnum)
				wordnum_arr.append(wordnum)

		print("extracted for surah:" + str(surahnum))

	df = pd.DataFrame({'arabicWord':arabic_word_arr})
	df['surahnum'] = surahnum_arr
	df['ayahnum'] = ayahnum_arr
	df['wordnum'] = wordnum_arr
	driver.close()
	return df

if __name__ == '__main__':
	list_of_jsons = []
	df = pd.read_json("cross_check_words_frequency.json")
	print(df)
	driver = webdriver.Chrome()
	dfall = get_all_words(driver)
	dfall.to_pickle("dfall.pkl")
	with open('dfall.pkl' , 'rb') as fp:
		dfall = pickle.load(fp)
	print(dfall)
	merged_inner = pd.merge(left = df, right = dfall, left_on=['surahnum','ayahnum','wordnum'], right_on=['surahnum','ayahnum','wordnum'])
	print(merged_inner)
	for i in merged_inner.index:
		word_json = {
						'question': merged_inner['arabicWord'][i],
						'answer': merged_inner['answer'][i],
						'surahnum' : int(merged_inner['surahnum'][i]),
						'ayahnum' : int(merged_inner['ayahnum'][i]),
						'wordnum' : int(merged_inner['wordnum'][i]),
						'frequency': int(merged_inner['frequency'][i]),
						'tlit' : merged_inner['tlit'][i]
					}
		list_of_jsons.append(word_json)
	with open('cross_final.json','w') as f:
		ujson.dump(list_of_jsons,f,ensure_ascii=False, indent=4)



