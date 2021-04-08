import requests
import csv

from psaw import PushshiftAPI
import pandas as pd


def raw_response():
    subreddit = "Conservative"
    amount = "1000"

    response = requests.get(
        "https://api.pushshift.io/reddit/search/submission/?size=" + amount + "&subreddit=" + subreddit)

    subimission_comment_ids = ""
    count = 0
    print("starting")
    for x in response.json()["data"]:
        response2 = requests.get("https://api.pushshift.io/reddit/submission/comment_ids/" + x["id"])
        count += 1
        if count % 10 == 0:
            print(count)
        for y in response2.json()["data"]:
            subimission_comment_ids += y + ","

    if subimission_comment_ids:
        subimission_comment_ids = subimission_comment_ids.rstrip(subimission_comment_ids[-1])
        response = requests.get("https://api.pushshift.io/reddit/search/comment/?ids=" + subimission_comment_ids)

        row_list = [["Id", "Date_Created_Utc", "Score", "Parent_id", "Body", "Link", "Mentioned Nouns",
                     "Sentiment-Subjectivity", "Sentiment-Polarization", "Hate Speech Level"]]
        for x in response.json()["data"]:
            row_list.append(
                [x["id"], x["created_utc"], x["score"], x["parent_id"], x["body"], x["permalink"], "", "", "", ""])
        row_list.append(["Total Comments:", len(row_list), "Total Posts:", count])
        with open(subreddit + '.csv', 'w', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(row_list)


def get_comments(filename="Conservative.csv", subreddit="conservative", limit=100):
    api = PushshiftAPI()
    gen = api.search_comments(subreddit=subreddit,
                              filter=["id", "created_utc", "score", "parent_id", "body", "permalink"], limit=limit)
    df = pd.DataFrame(data.d_ for data in gen)
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    get_comments()
