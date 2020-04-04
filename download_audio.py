import urllib.error
import wget
import time
from constants import (
    NUM_SURAHS_IN_QURAN, 
    NUM_ROOT_WORDS_IN_CORPUS,
    ALL_AYAHS,
    MAX_AYAHS_IN_A_SURAH,
    MAX_WORDS_IN_AN_AYAH
)

def get_audio():
    baseurl = 'https://verses.quran.com/wbw/' # '001_001_100.mp3'
    start_time = time.time()
    for x in range(1, NUM_SURAHS_IN_QURAN + 1):
        for y in range(1, MAX_AYAHS_IN_A_SURAH + 1):
            for z in range(1, MAX_WORDS_IN_AN_AYAH + 1):
                elapsed_time = time.time() - start_time
                print(str(round(elapsed_time)) + " " + "seconds elapsed")
                surah = append0s(x)
                ayah = append0s(y)
                word = append0s(z)
                try:
                    url = baseurl + surah + "_" + ayah + "_" + word + ".mp3"
                    wget.download(url)
                    print("\n" + surah + "_" + ayah + "_" + word + ".mp3")
                    time.sleep(1)
                except urllib.error.HTTPError:
                    print("ERROR: " + url)
                    break


def append0s(number):
    ret = str(number)
    if len(ret) == 1:
        ret = '00' + ret
    elif len(ret) == 2:
        ret = '0' + ret
    return ret

if __name__== "__main__":

    get_audio()
