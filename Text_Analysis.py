import spacy
from spacytextblob.spacytextblob import SpacyTextBlob  # noqa:F401
from hatesonar import Sonar
import pandas as pd
from multiprocessing import Process


def run_data_analysis(filename):
    print("Beginning to Analyze " + filename)

    # Load model and load textblob into pipeline
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("spacytextblob")

    # Load csv file to dataframe data
    data = pd.read_csv(filename)

    # Change the Mentioned Nouns column to be a string instead of float
    data["Mentioned Nouns"] = data["Mentioned Nouns"].astype(str)

    # Iterate through the csv, feeding each string to spacy and setting the corresponding columns
    for i in range(data.shape[0] - 1):
        # Load body with the body of the comment and tokenize it, put it in doc
        body = data["Body"].iloc[i]
        doc = nlp(body)

        # If comment is removed, deleted, or written by a bot, set everything to 0 or empty
        if (
            data.at[i, "Body"] == "[removed]"
            or data.at[i, "Body"] == "[deleted]"
            or "I am a bot, and this action was performed automatically." in data.at[i, "Body"]
        ):
            data.at[i, "Sentiment-Subjectivity"] = 0
            data.at[i, "Sentiment-Polarization"] = 0
            data.at[i, "Mentioned Nouns"] = ""
            data.at[i, "Hate Speech Level"] = 0

        # If not removed, deleted, or written by a bot, then analyze it
        else:
            # Hate sonar stuff
            sonar = Sonar()
            if sonar.ping(body)["top_class"] == "neither":
                topclass = 0
            elif sonar.ping(body)["top_class"] == "offensive_language":
                topclass = 1
            elif sonar.ping(body)["top_class"] == "hate_speech":
                topclass = 2
            data.at[i, "Hate Speech Level"] = topclass

            # Set the subjectivity and polarity with the automatically calculated texblob values
            data.at[i, "Sentiment-Subjectivity"] = doc._.subjectivity
            data.at[i, "Sentiment-Polarization"] = doc._.polarity

            # All allowed entities to be put in mentioned nouns
            allowed_entities = [
                "PERSON",
                "ORG",
                "WORK_OF_ART",
                "GPE",
                "NORG",
                "LOC",
                "LAW",
                "LANGUAGE",
                "PRODUCT",
                "FAC",
            ]

            nouns = []

            # Get all nouns with the allowed entities, put it in nouns
            for ent in doc.ents:
                if ent.label_ in allowed_entities and ent.text not in nouns:
                    nouns.append(ent.text)

            # Get all noun phrases and put it in nouns, remove any stop words and punctiation, they're just noise
            phrases = []
            for phrase in doc.noun_chunks:
                for word in phrase:
                    if not word.is_stop and not word.is_punct:
                        phrases.append(word.text)

                if phrases:
                    if phrases[0] not in nouns and phrases[0].lower() != 'i':
                        nouns.append(' '.join(phrases))
                phrases = []

            # Get all pronouns that aren't me, myself, and I
            for token in doc:
                if (
                    token.pos_ == "PROPN"
                    and token.text.lower() != "me"
                    and token.text.lower() != "myself"
                    and token.text.lower() != "i"
                ):
                    if data.at[i, "Parent_id"] not in nouns:
                        nouns.append(data.at[i, "Parent_id"])

            # Pour the nouns in the column
            data.at[i, "Mentioned Nouns"] = ", ".join(nouns)

    # Output to this csv for now
    data.to_csv(filename, index=False)
    print("Completed the Analysis of " + filename)

if __name__ == "__main__":
    run_data_analysis('Conservative.csv')

