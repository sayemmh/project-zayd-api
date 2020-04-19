# insert json documents for words in context into mongodb cluster
#!/bin/bash
SECRETS_LOC="/Users/sayemhoque/Documents/project-zayd-data/bash-scripts/sayem.secrets"
MONGO_DB_NAME="surahs-words"
LOCAL_DIR="/Users/sayemhoque/Documents/project-zayd-data/json-surah-words/"
COLLECTION_NAME="words-in-context"

source $SECRETS_LOC
cd json-surah-words
echo $(ls)

for file in *.json
do
  sed '$d' < $file | sed "1d" > temp
  sed -i '.bak' 's/},/}/g' temp
  cat temp

  mongoimport --host Cluster0-shard-0/cluster0-shard-00-00-hbqdc.mongodb.net:27017,cluster0-shard-00-01-hbqdc.mongodb.net:27017,cluster0-shard-00-02-hbqdc.mongodb.net:27017 --ssl --username $MONGO_USER --password $MONGO_PW --authenticationDatabase admin --db $MONGO_DB_NAME --collection $COLLECTION_NAME --type JSON --file $LOCAL_DIR/temp
  
  rm -rf temp*

  echo "----"
done

