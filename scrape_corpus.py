from bs4 import BeautifulSoup
import requests
import pickle
import time
import csv
import pandas as pd
from collections import Counter

'''
downloads / serializes all 1665 root words from corpus.quran.com and saves in pckl-words/ directory
* do not remove time.sleep() or requests will time out *
run time is ~15 minutes
'''



def visit_page(morphology):
    base = "http://corpus.quran.com/qurandictionary.jsp" + morphology
    page_response = requests.get(base , timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    return page_content

visited = []
to_visit = ['?q=A%5Edam']
count = 0

while len(to_visit) != 0:
    wordmorphologies = []
    definition = []
    pronunciations = []
    arabicAyah = []
    arabicWord = []
    wordFormInfo = []
    wordFormTypes = []
    wordFormTlits = []
    wordForms = []
    wordFormDefs = []


    l = []
    time.sleep(0.5)

    morphology = to_visit.pop(0)
    visited.append(morphology)
    page_content = visit_page(morphology)

    for hl in page_content.find_all("a"):
        if hl['href'][0:18] == "wordmorphology.jsp":
            # content
            wordmorphologies.append(hl['href'])
            # content
            definition.append(hl.text)
        if hl['href'][0] == '?' and len(wordmorphologies) != 0:
            if hl['href'] not in to_visit and hl['href'] not in visited:
                to_visit.append(hl['href'])
    for i in page_content.find_all("i"):
        # content
        pronunciations.append(i.text)
    for x in page_content.find_all("td", {"class": "c3"}):
        # content
        arabicAyah.append(x.text)
        for y in x.find_all("span"):
            # content
            arabicWord.append(y.text)
    count = count + 1

    rootWord = page_content.find_all("span", {"class": "at"})[0].text
    rootWordType = str(page_content.find_all("p", {"class": "dsm"})[0]).split('The')[1].split('<i')[0].strip()
    

    wordVars = page_content.find_all("h4", {"class":"dxe"})
    for wordFormVars in wordVars:
        wordFormEng = (str(wordFormVars.string)).split("-")[0].strip()
        if len((str(wordFormVars.string)).split("-")) < 2:
            wordFormDef = definition[0]
        else:
            wordFormDef = (str(wordFormVars.string)).split("-")[1].strip()
        wordFormInfo.append((wordFormEng, wordFormDef))

    # isolates unordered list of word forms and their frequency 
    if len(wordFormInfo) > 1:
        wordInfo = page_content.find_all("ul",{"class":"also"})[0]
        i = 0
        for nextChild in wordInfo.findChildren():
            if nextChild.name == 'li':
                wordFormTlit = nextChild.find_all("i")[0].text
                wordFormArabic = nextChild.find_all("span")[0].text
                wordFormInfo[i] = wordFormInfo[i] + (wordFormTlit,wordFormArabic)
                i = i + 1
    elif "root" in rootWord:
        wordFormTlit = page_content.find_all("p",{"class":"dsm"})[0].find_all("i", {"class":"ab"})[1].text
        wordFormArabic = page_content.find_all("p",{"class":"dsm"})[0].find_all("span", {"class":"at"})[1].text
    else:
        wordFormTlit = page_content.find_all("i",{"class":"ab"})[0].text
        wordFormArabic = rootWord
        wordFormInfo[0] = wordFormInfo[0] + (wordFormTlit,wordFormArabic)
    wordVarBlocks = str(page_content.prettify()).split('<h4 class="dxe">')[1:]
    for i , wordVarBlock in enumerate(wordVarBlocks):
        wordVarColl = BeautifulSoup(wordVarBlock, "html.parser")
        wordVarColl.find_all("p", {"class":"dxt"})

        if len(wordVarColl.find_all("p",{"class":"dxt"})) > 0:
            wordVarSubTypes = wordVarColl.find_all("table",{"class":"taf"})
            for j, wordVarSubType in enumerate(wordVarSubTypes):
                wordVarTypeAppend = str(wordVarColl.find_all("p", {"class":"dxt"})[j].text).strip()
                for wordVarInSubType in wordVarSubType.find_all("td",{"class":"c1"}):
                    wordFormTypes.append(wordFormInfo[i][0] + ' (' + wordVarTypeAppend[4:] + ')')
                    wordFormDefs.append(wordFormInfo[i][1])
                    wordFormTlits.append(wordFormInfo[i][2])
                    wordForms.append(wordFormInfo[i][3])
        else:
            for wordVarEntry in wordVarColl.find_all("td",{"class":"c1"}):
                wordFormTypes.append(wordFormInfo[i][0])
                wordFormDefs.append(wordFormInfo[i][1])
                wordFormTlits.append(wordFormInfo[i][2])
                wordForms.append(wordFormInfo[i][3])

    diff = len(pronunciations) - len(definition)
    pronunciations = pronunciations[diff:len(pronunciations)]

    # print(Counter(pronunciations))
    #print(diff)

    if (diff == 1):
        rootWordPronunciation = pronunciations[0]
    elif (diff == 2):
        rootWordPronunciation = pronunciations[0]
    else:
        rootWordPronunciation = Counter(pronunciations).most_common(1)[0][0]
    # print(rootWordPronunciation)
    # print(diff)

    df = pd.DataFrame({'arabicWord':arabicWord})
    df['pronunciations'] = pronunciations
    df['definition'] = definition
    df['arabicAyah'] = arabicAyah
    df['wordmorphologies'] = wordmorphologies
    df['rootWord'] = rootWord
    df['rootWordType'] = rootWordType
    df['wordForms'] = wordForms
    df['wordFormDefs'] = wordFormDefs
    df['wordFormTlits'] = wordFormTlits
    df['wordFormTypes'] = wordFormTypes
    print(df)

    # df.iloc[:, 0:3]


    with open("pckl-words/" + str(count) + ".pckl", "wb") as fp:
        pickle.dump(df, fp)

    df.to_csv("csv/" + rootWord + '.csv', sep=',', encoding='utf-8')