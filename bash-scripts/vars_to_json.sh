#!/bin/bash
LOCAL_DIR="/Users/sayemhoque/Documents/project-zayd-data/json-surah-words/"

cd json-surah-words

for file in *.json
do
  sed '$d' < $file | sed "1d" > file
  sed 's/;//g' file > $file
done
