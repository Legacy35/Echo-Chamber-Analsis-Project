import spacy
from spacy import displacy
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd

# Load model and load textblob into pipeline
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')

# Load csv file to dataframe data
data = pd.read_csv('Conservative.csv')

# Delete any [removed] or [deleted] data
data.drop(data.index[data['Body'] == '[removed]'], inplace = True)
data.drop(data.index[data['Body'] == '[deleted]'], inplace = True)

# Change the Mentioned Nouns column to be a string instead of float
data['Mentioned Nouns'] = data['Mentioned Nouns'].astype(str)

# Iterate through the csv, feeding each string to spacy and setting the corresponding columns
for i in range(data.shape[0] - 1):
    doc = nlp(data['Body'].iloc[i])
    data.at[i, 'Sentiment-Subjectivity'] = doc._.subjectivity
    data.at[i, 'Sentiment-Polarization'] = doc._.polarity

    nouns = []
    for token in doc:
        if token.pos_ == 'NOUN' or token.pos_ == 'PROPN':
            nouns.append(token.text)
    
    data.at[i, 'Mentioned Nouns'] = ', '.join(nouns)

# Output to this csv for now
data.to_csv("Output.csv", index=False)
