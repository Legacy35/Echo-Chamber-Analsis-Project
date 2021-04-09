import spacy
import os
from spacy import displacy
from spacytextblob.spacytextblob import SpacyTextBlob
import pandas as pd

filename = 'before.csv'

# Load model and load textblob into pipeline
nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')

# Load csv file to dataframe data
data = pd.read_csv('Conservative.csv')

data['Mentioned Nouns'] = data['Mentioned Nouns'].astype(str)
#data['Entities'] = data['Mentioned Nouns']

data.drop(['Id', 'Date_Created_Utc', 'Score', 'Parent_id', 'Link'], axis = 1, inplace = True)

for i in range(data.shape[0] - 1):
    if data.at[i, 'Body'] == '[removed]' or data.at[i, 'Body'] == '[deleted]':
        data.at[i, 'Sentiment-Subjectivity'] = 0
        data.at[i, 'Sentiment-Polarization'] = 0
        data.at[i, 'Mentioned Nouns'] = ''

    doc = nlp(data['Body'].iloc[i])
    data.at[i, 'Sentiment-Subjectivity'] = doc._.subjectivity
    data.at[i, 'Sentiment-Polarization'] = doc._.polarity

    # nouns = []
    # entities = []
    # for ent in doc.ents:
    #     if ent.label_ != 'PERCENT' and ent.label_ != '':
    #         nouns.append(ent.text)
    #         entities.append(ent.label_)
    
    # for token in doc:
    #     if token.ent_type_ == '' and (token.pos_ == 'NOUN' or token.pos_ == 'PRON'):
    #         if token.text.lower() != 'i' and token.text.lower() != 'me':
    #             nouns.append(token.text)

    # data.at[i, 'Mentioned Nouns'] = ', '.join(nouns)
    # data.at[i, 'Entities'] = ', '.join(entities)

    nouns = []
    for token in doc:
        if token.pos_ == 'NOUN' or token.pos_ == 'PROPN':
            nouns.append(token.text)
    
    data.at[i, 'Mentioned Nouns'] = ', '.join(nouns)

if os.path.exists(filename):
    os.remove(filename)

data.to_csv(filename, index = False)