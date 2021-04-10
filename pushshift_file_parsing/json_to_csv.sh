#!/bin/bash
# Instal ripgrep and jq
# Take in Pushshift raw files and output them into a CSV file
FILENAME=RC_2016-11

# Comment to unpack
#bunzip2 -f -k -v $FILENAME.bz2
# mv -f $FILENAME $FILENAME.json

subreddits=("The_Donald" "LateStageCapitalism" "Republican" "Republican" "republicans" "Democrat" "democrats" "socialism" "politics" "news")
for i in "${subreddits[@]}"
do
  echo "Formatting subreddit:$i from json into csv"
  # This is brutally slow, use grep to filter out strings instead
  #jq ". |
  #    select( .subreddit == \"$i\" ) |
  #    [.name, .parent_id, .subreddit, .link_id, .author,.created_utc, .score, .body] | @csv" "${FILENAME}.json" > "${FILENAME}_$i.csv"
  rg --ignore-case "\"subreddit\":\"$i\"" "${FILENAME}.json" | jq ". | [.id, .name, .parent_id, .subreddit, .link_id, .author,.created_utc, .score, .body] | @csv" > "${FILENAME}_$i.csv"
done

7za a ${FILENAME}_subreddits.7z ${FILENAME}_*.csv
