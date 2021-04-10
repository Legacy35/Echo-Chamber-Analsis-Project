#!/bin/bash
# Take in Pushshift raw files and output them into a CSV file
FILENAME=RC_2016-11

# Comment to unpack
bunzip2 -f -k -v $FILENAME.bz2
mv -f $FILENAME $FILENAME.json

subreddits=("conservative" "socialism" "politics" "republican" "news" "lateStageCapitalism")
for i in "${subreddits[@]}"
do
  echo "Parsing out \"subreddit\":\"$i\""
  grep "\"subreddit\":\"$i\"" $FILENAME.json > "${FILENAME}_$i.json"
  # head -n 1000 FILENAME.json | grep "\"subreddit\":\"$i\"" > "${FILENAME}_$i.json"
  echo "Formatting subreddit:$i from json into csv"
  jq --raw-output '. | [.name, .parent_id, .link_id, .author,.created_utc, .score, .body] | @csv' "${FILENAME}_$i.json" > "${FILENAME}_$i.csv"
done

7za a ${FILENAME}_csv.7z ${FILENAME}_*.csv