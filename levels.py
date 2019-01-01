from bs4 import BeautifulSoup
import requests
import pickle
import time

###
# out is a 2-d list where each inner list is a key, # of occurrences pair for each arabic root word
#
###

levels = []
for num in range(1, 1665):
    with open('word/' + str(num) + '.pckl', 'rb') as fp:
         l = pickle.load(fp)
    levels.append([num, len(l[0])])

with open("levels.pckl", "wb") as fp:
    pickle.dump(levels, fp)

total_words = [sum(x) for x in zip(*levels)][1]
print(total_words)
