import spacy
from spacy import displacy
from spacytextblob.spacytextblob import SpacyTextBlob
from hatesonar import Sonar
import pandas as pd
from multiprocessing import Process

def run_data_analysis(filename):
    print("Begining to Analyze "+ filename)
    # Load model and load textblob into pipeline
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob')

    # Load csv file to dataframe data
    data = pd.read_csv(filename)

    # Change the Mentioned Nouns column to be a string instead of float
    data['Mentioned Nouns'] = data['Mentioned Nouns'].astype(str)
    
    # Iterate through the csv, feeding each string to spacy and setting the corresponding columns
    for i in range(data.shape[0] - 1):
        body = data['Body'].iloc[i]
        doc = nlp(body)
        if data.at[i, 'Body'] == '[removed]' or data.at[i, 'Body'] == '[deleted]'or "I am a bot, and this action was performed automatically." in data.at[i, 'Body']  :
            data.at[i, 'Sentiment-Subjectivity'] = 0
            data.at[i, 'Sentiment-Polarization'] = 0
            data.at[i, 'Mentioned Nouns'] = ''
            data.at[i, 'Hate Speech Level'] = 0
        else:
            sonar=Sonar()
            if sonar.ping(body)['top_class'] == 'neither':
                topclass=0
            elif sonar.ping(body)['top_class'] == 'offensive_language':
                topclass=1
            elif sonar.ping(body)['top_class'] == 'hate_speech':
                topclass=2
            data.at[i, 'Hate Speech Level'] = topclass

            data.at[i, 'Sentiment-Subjectivity'] = doc._.subjectivity
            data.at[i, 'Sentiment-Polarization'] = doc._.polarity

            nouns = []
            for token in doc:
                if token.pos_ == 'NOUN':
                    if token.text not in nouns:
                        nouns.append(token.text)
                if token.pos_ == 'PROPN' and token.text != "me"and token.text != "myself" and token.text != "I":
                        if data.at[i, 'Parent_id'] not in nouns:
                            nouns.append(data.at[i, 'Parent_id'])
            
            data.at[i, 'Mentioned Nouns'] = ', '.join(nouns)

    # Output to this csv for now
    data.to_csv(filename, index=False)
    print("Completed the Analysis of "+ filename)

if __name__ == "__main__":
    # construct a different process for each function
    run_data_analysis("RC_2016-11_Democrat.csv")
