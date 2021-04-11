import pandas as pd
import numpy as np
import math

def Data_Analysis(filename):
    df = pd.read_csv(filename)
    rows, cols = (0, 0)
    arr = [[0]*cols]*rows
    arrH = []
    noun_index = {}
    arrW = []
    val = np.nan
    count =0
    print("Starting to read Noun Sentiments")
    for index, row in df.iterrows():
        if row['Body'] != '[removed]' and row['Body'] != '[deleted]'and "I am a bot, and this action was performed automatically." not in row['Body']:
            if not pd.isnull(row["Hate Speech Level"]):
                arrH.append(row["Hate Speech Level"])
            if not pd.isnull(row["Mentioned Nouns"]):
                nouns = row["Mentioned Nouns"].split(",")
                for noun in nouns:
                    if noun not in noun_index:
                        noun_index[noun]=len(arr)
                        arrW.append(0)
                        arr.append([])
                    arr[noun_index.get(noun)].append(row["Sentiment-Polarization"])
                    arrW[noun_index[noun]]= arrW[noun_index[noun]]+1
                    count = count +1

                
    print("Noun Sentiment's Read")
    print("Starting Standard deviation calculation")
    arr2= []
    for x in arr:
        arr2.append(np.std(x))
    print("Standard deviation calculation Completed")
    avg = 0

    for i in range(len(arrW)):
        arrW[i] = arrW[i]/count

    for i in range(len(arr2)):
        arr2[i] = arrW[i]*arr2[i]

    AverageWeighted = sum(arr2)/len(arr2)
    AverageH = sum(arrH)/len(arrH)
    print (filename)
    print("Weighted Average: ")
    print(AverageWeighted)
    print("Average Hate Speech: ")
    print(AverageH)

if __name__ == "__main__":
    Data_Analysis("conservative.csv")
    Data_Analysis("lateStageCapitalism.csv")
    Data_Analysis("news.csv")
    Data_Analysis("politics.csv")
    Data_Analysis("republican.csv")
    Data_Analysis("socialism.csv")
