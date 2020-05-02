import urllib.error
import wget
import time
from constants import (
    NUM_SURAHS_IN_QURAN,
    MAX_AYAHS_IN_A_SURAH,
    MAX_WORDS_IN_AN_AYAH
)
LOCAL_DIR = "/root/project-zayd-data/audio/"
# LOCAL_DIR = "/Users/sayemhoque/Documents/project-zayd-data/"

def get_audio():
    baseurl = 'https://verses.quran.com/wbw/' # '001_001_100.mp3'
    start_time = time.time()
    for x in range(1, NUM_SURAHS_IN_QURAN + 1):
        for y in range(1, MAX_AYAHS_IN_A_SURAH + 1):
            z = 1 # wordnum
            w = 1 # quran.com file num
            while w < MAX_WORDS_IN_AN_AYAH + 1:
                elapsed_time = time.time() - start_time
                print(str(round(elapsed_time)) + " " + "seconds elapsed")
                surah = append0s(x)
                ayah = append0s(y)
                word = append0s(z)
                filenum = append0s(w)
                try:
                    url = baseurl + surah + "_" + ayah + "_" + filenum + ".mp3"
                    filename = LOCAL_DIR + surah + "_" + ayah + "_" + word + ".mp3"
                    wget.download(url, out=filename)
                    print("\n" + surah + "_" + ayah + "_" + word + ".mp3")
                    time.sleep(1)
                    z += 1
                    w += 1
                except urllib.error.HTTPError:
                    print("ERROR: " + url)
                    print("Trying next url")
                    w += 1
                    print("filenum: " + filenum + " _ wordnum: " + word)
                    if z == 1:
                        break
                    if w > z + 15:
                        break
    print("finished")

def append0s(number):
    ret = str(number)
    if len(ret) == 1:
        ret = '00' + ret
    elif len(ret) == 2:
        ret = '0' + ret
    return ret

if __name__== "__main__":

    get_audio()
