import pickle
import time

###
# out is a 2-d list where each inner list is a key, # of occurrences pair for each arabic root wordx
#
###

def open_word(key):
    with open('pckl-words/' + str(key) + '.pckl', 'rb') as fp:
        l = pickle.load(fp)
        # print(l)
    return l

# counts = []
# for num in range(1, 1665):
#     with open('pckl-words/' + str(num) + '.pckl', 'rb') as fp:
#          l = pickle.load(fp)
#     counts.append([num, len(l[0])])
#
#
# counts.sort(key=lambda x:x[1], reverse=True)
# print(counts)
# with open("counts.pckl", "wb") as fp:
#     pickle.dump(counts, fp)
#
# with open("counts.pckl", "rb") as fp:
#     counts = pickle.load(fp)
#
# # total word count
# total_word_count = [sum(x) for x in zip(*counts)][1]
# print(total_word_count)
#
# # top 5 root words in corpus
# counts[:5]
# >>> [[61, 2851], [1245, 1722], [59, 1464], [1305, 1390], [524, 980]]
# w1 = open_word(61)
# print(w1[2])
# w1
# ['your God',
#  'and (the) God',
#  'God',
#  'And your God',...]
# w2 = open_word(1245)
# w2[1][1], w2[2][1], w2[4][1]
#
#
# # ['say',
# #  'it is said',
# #  'they say',
# #  'it is said',
# #  'they say',
# #  'they say',
# #  'they say',
# w3 = open_word(59)[1]
# w3
# # ['(of) those',
# #  'Those who',
# #  'And those who',
# #  'those who',
# #  'and those who',
# #  'those who',
# #  '(are) the ones who',
# w4 = open_word(1305)[1]
# w4
#
#

# print(open_word(91))
for i in range(21, 1000, 3):
    try:
        w = open_word(i)
        # print('{',
        #         'question:'+ '\''+ w[4][50]+'\''+ ','+
        #         'answer:'+ '\''+ w[1][50]+'\''+ ','+
        #         'qid:'+ str(i) + ','+
        #         'tlit:'+ '\''+ w[2][50]+'\'',
        #         '}'+ ',')

        print('\''+w[1][50]+'\''+',')
    except IndexError:
        pass
