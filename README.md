# Echo-Chamber-Analysis-Project
ML and Network analytics Project

The underneath code snippet is meant to setup the enviornment to run the project.


## Setup

```bash
python -m venv .venv
# Windows
source .venv/Scripts/activate
# Linux
source .venv/bin/activate
pip install -U setuptools wheel
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m textblob.download_corpora
```


# Developing

Check code before committing with pre-commits. This runs a script to auto format code before you commit.
This is not needed to run the project.
```bash
# Windows
source .venv/Scripts/activate
# Linux
source .venv/bin/activate
pip install pre-commit
pre-commit install
# Run on all files
pre-commit run --all-files
```


## Running the code
First: `python Data_Ingestion.py`
In the Data Ingestion file enter the name of the subreddit and the amount of posts you want to get in the main method.
By default, it will pull 10 comments from six subreddit we studied.
It will then automatically analyze all the comments after it has pulled all the data.
The analysis code is in `Text_Analysis.py`.
This outputs a csv file with the subreddits name. This includes information on sentiment and hate speech.

Second: `python Data_Analysis.py`
Run the Data analysis, in the main method instert the file names of csv files recieved from the first part.
This runs our original method to detect echo chambers on subreddit s.
It works by looking at the nouns and assigning sentiment to them. Once sentiment is assigned we look at distributions.
It will then output in console all the data from the subreddit analysis.

