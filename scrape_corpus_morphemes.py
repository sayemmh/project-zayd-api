# scrapes all word morphemes for every single ayah
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import ujson
import urllib
from constants import NUM_SURAHS_IN_QURAN, NUM_ROOT_WORDS_IN_CORPUS, ALL_AYAHS


def getHyperlinks(surahNum):
    hyperlinkArr = []
    base = 'http://corpus.quran.com/wordbyword.jsp?chapter=' + str(surahNum)
    page_content = getPageContent(base)
    verseSelect = page_content.find_all("select", {"name":"verseList"})
    verseArr = verseSelect[0].find_all("option")
    for verse in verseArr:
        hyperlinkArr.append(base  + "&verse=" + verse.text.split("(")[1].split(":")[1].split(")")[0])
    return hyperlinkArr

def getPageContent(hyperlink):
    page_response = requests.get(hyperlink, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    return page_content

def getAyahNum(wordRow):
    return wordRow.find_all("td")[0].find("span").text.split(":")[1]
def getWordNum(wordRow):
    return wordRow.find_all("td")[0].find("span").text.split(":")[2].split(")")[0]

def getImage(wordRow, surahNum, ayahNum, wordNum):
    imageHyperlinkID = str(wordRow.find_all("td")[1].find_all("img")[-1]).split("wordimage?id=")[1].split("\"")[0]
    imageHyperlink = "http://corpus.quran.com/wordimage?id=" + imageHyperlinkID
    resource = urllib.request.urlopen(imageHyperlink)
    with open("word-images/" + str(surahNum) + "_" + str(ayahNum) + "_" + str(wordNum) + ".png", "wb") as image:
        image.write(resource.read())
        image.close()
def getEngBreakdown(wordRow):
    morphemeArray =[]
    morphemeCodes = wordRow.find_all("td")[2].find_all("b")
    for morphemeCode in morphemeCodes:
        morphemeCodeColor = morphemeCode["class"]
        morphemeArray.append([morphemeCode.text, morphemeCodeColor[0]])
    morphemeDescs = str(wordRow.find_all("td")[2]).split("<div")[0].split("<br/>")
    for i, morphemeDesc in enumerate(morphemeDescs):
        morphemeDesc = BeautifulSoup(morphemeDesc, "html.parser")
        morphemeDesc = morphemeDesc.text.split("–")[1].strip()
        morphemeArray[i].append(morphemeDesc)
    return morphemeArray

def getArabicBreakdown(wordRow):
    morphemeArabicDescs = str(wordRow.find_all("div",{"class":"arabicGrammar"})).split("<div class=\"arabicGrammar\">")[1].split("</div>")[0].split("<br/>")
    morphemeArabicArray = []
    for morphemeArabicDesc in morphemeArabicDescs:
        morphemeArabicArray.append(morphemeArabicDesc)
    return morphemeArabicArray

def build_jsons_for_all_ayahs():
    list_of_jsons = []  
    for surahNum in range(1, NUM_SURAHS_IN_QURAN+1):
        ayahNum = 0
        hyperlinkArr = getHyperlinks(surahNum)
        for count, hyperlink in enumerate(hyperlinkArr):
            if ayahNum > count:
                continue 
            page_content = getPageContent(hyperlink)
            wordTable = page_content.find_all("table",{"class":"morphologyTable"})[0]
            wordRows = wordTable.find_all("tr", {"class": None})
            for wordRow in wordRows:
                if wordRow.has_attr("class"):
                    continue
                ayahNum = int(getAyahNum(wordRow))
                wordNum = int(getWordNum(wordRow))
                print("Building for surah: " + str(surahNum) + ", Ayah: " + str(ayahNum)+ ", Word: " + str(wordNum))
                # getImage(wordRow, surahNum, ayahNum, wordNum)
                morphemeEng = getEngBreakdown(wordRow)
                morphemeArabic = getArabicBreakdown(wordRow)
                word_json = {
                                'surahnum': surahNum,
                                'ayahnum': ayahNum,
                                'wordnum': wordNum,
                                'morphemeEnglishList': morphemeEng,
                                'morphemeArabicList':morphemeArabic
                            }
                list_of_jsons.append(word_json)
        with open('all_words_morphemes.json','w') as f:
            ujson.dump(list_of_jsons,f,ensure_ascii=False, indent=4)
            f.close()
if __name__ == '__main__':
    build_jsons_for_all_ayahs()

