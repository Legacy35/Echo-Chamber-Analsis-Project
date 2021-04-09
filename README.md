# Echo-Chamber-Analysis-Project
ML and Network analytics Project

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U setuptools wheel
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m textblob.download_corpora
```

Check code before committing with pre-commits
```bash
pip install pre-commit
pre-commit install
# Run on all files
pre-commit run --all-files
```

## CLI
```
psaw -q "cats" -s askreddit -l 100 -o cats_test.csv
```
