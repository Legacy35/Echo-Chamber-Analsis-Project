
import requests
import json
import csv

subreddit="Conservative"
amount= "1000"

response = requests.get("https://api.pushshift.io/reddit/search/submission/?size="+amount+"&subreddit="+subreddit)

subimission_comment_ids =""
count =0
print("starting")
for x in response.json()["data"]:
    response2 = requests.get("https://api.pushshift.io/reddit/submission/comment_ids/"+ x["id"])
    count+=1
    if count%10==0:
        print(count)
    for y in response2.json()["data"]:
        subimission_comment_ids+=y + ","

if subimission_comment_ids:
    subimission_comment_ids = subimission_comment_ids.rstrip(subimission_comment_ids[-1])
    response = requests.get("https://api.pushshift.io/reddit/search/comment/?ids="+subimission_comment_ids)
 
    row_list = [["Id","Date_Created_Utc","Score","Parent_id","Body","Link", "Mentioned Nouns", "Sentiment"]]
    for x in response.json()["data"]:
        row_list.append([x["id"],x["created_utc"],x["score"],x["parent_id"],x["body"],x["permalink"], "",""])
    row_list.append(["Total Comments:",len(row_list), "Total Posts:", count])
    with open(subreddit+'.csv', 'w', newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(row_list)