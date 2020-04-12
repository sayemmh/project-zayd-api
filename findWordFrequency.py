import pandas as pd 
import ujson
import json

def find_word_frequency(filename):
	list_of_jsons = []
	with open(filename, 'r') as f:
		json_data = f.read()
	newWords = json.loads(json_data)
	df = pd.read_json("cross_check_words_2.json")
	freqDict = df['tlit'].value_counts().to_dict()
	for newWord in newWords:
		tlit = newWord['tlit']
		newWord.update(frequency= freqDict.get(tlit))
		list_of_jsons.append(newWord)
	with open("cross_check_words_frequency.json", 'w') as fw:
		ujson.dump(list_of_jsons,fw,ensure_ascii=False, indent=4)
		fw.close()
	


if __name__ == '__main__':
    find_word_frequency("cross_check_words_2.json")
