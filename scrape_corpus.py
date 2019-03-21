from bs4 import BeautifulSoup
import requests
import pickle
import time
import csv

#####
# downloads / serializes all 1665 root words from corpus.quran.com and saves in pckl-words/ directory
# * do not remove time.sleep or requests will time out *
# run time is ~15 minutes
#####

letterHomes = ['?q=A','?q=b','?q=t','?q=v','?q=j','?q=H','?q=x','?q=d','?q=*','?q=r','?q=z','?q=s','?q=$','?q=S','?q=D','?q=T','?q=Z','?q=E','?q=g','?q=f','?q=q','?q=k','?q=l','?q=m','?q=n','?q=h','?q=w','?q=y']

letterHomes = ['?q=A']

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
    text = []
    pronunciations = []
    arabicAyah = []
    arabicWord = []
    l = []
    time.sleep(1)

    morphology = to_visit.pop(0)
    visited.append(morphology)
    page_content = visit_page(morphology)

    for hl in page_content.find_all("a"):
        if hl['href'][0:18] == "wordmorphology.jsp":
            # content
            wordmorphologies.append(hl['href'])
            # content
            text.append(hl.text)
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

    # print(pronunciations)
    l.append(wordmorphologies)
    l.append(text)
    l.append(pronunciations)
    l.append(arabicAyah)
    l.append(arabicWord)
    count = count + 1
    print(l)
    with open("pckl-words/" + str(count) + ".pckl", "wb") as fp:
        pickle.dump(l, fp)

    data = [wordmorphologies, text]
    with open('csv/' + str(count) + '.csv', 'w') as f:
        writer = csv.writer(f)
        for row in zip(*data):
            writer.writerow(zip(arabicAyah, arabicWord))
