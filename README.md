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

Check code before committing with pre-commits
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
First:
In the Data Ingestion file enter the name of the subreddit and the amount of posts you want to get in the main method
It will then automatically analyze all the comments after it has pulled all the data
This outputs a csv file with the subreddits name

Second:
Run the Data analysis with the file names of csv files recieved from the first part
It will then output in console all the data from the subreddit analysis

