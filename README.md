# Echo-Chamber-Analysis-Project
ML and Network analytics Project

## Setup


```
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install psaw
$ pip install -U setuptools wheel
$ pip install -U spacy
$ python -m spacy download en_core_web_sm
$ pip install spacytextblob
$ python -m textblob.download_corpora
```

## CLI
```
psaw -q "cats" -s askreddit -l 100 -o cats_test.csv
```
