#!/bin/bash
LOCAL_DIR="/Users/sayemhoque/Documents/project-zayd-data/json-surah-words/"

cd json-surah-words

find . -type f -name '*.json' -exec sed -i '' s/true/True/ {} +
