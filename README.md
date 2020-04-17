## install

git clone https://github.com/sayemmh/project-zayd-data

create virtualenv

`pip3 install -r requirements.txt`

<br>

## scripts:

`scrape_corpus.py`:

scrapes http://corpus.quran.com/qurandictionary.jsp and outputs 1664 root words to `pckl/` and `csv/`

`wordsFromSurah.py`:

reads 1664 root words from `pckl/` and outputs 114 files containing json objects with every word found in each surah to `/json-surah-words`.
