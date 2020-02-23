import urllib.error
import wget
import time

def get_audio():
    baseurl = 'https://verses.quran.com/wbw/' # '001_001_100.mp3'
    # start_time = time.time()
    for x in range(64, 114 + 1):
        for y in range(1, 286 + 1):
            for z in range(1, 142 + 1):
                # elapsed_time = time.time() - start_time
                # print(str(round(elapsed_time)) + " " + "seconds elapsed")
                surah = append0s(x)
                ayat = append0s(y)
                part = append0s(z)
                try:
                    url = baseurl + surah + "_" + ayat + "_" + part + ".mp3"
                    wget.download(url)
                    print("\n" + surah + "_" + ayat + "_" + part + ".mp3")
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
