# chexpert-labeler
CheXpert NLP tool to extract observations from radiology reports.

## Prerequisites
Clone the [NegBio repository](https://github.com/ncbi-nlp/NegBio):

`git clone git@github.com:ncbi-nlp/NegBio.git`

Add the NegBio repository to your `PYTHONPATH`:

`export PYTHONPATH={path to clone repository}:$PYTHONPATH`

Make the virtual environment:

`conda env create -f environment.yml`

Install NLTK data:

`python -m nltk.downloader universal_tagset punkt wordnet`

Download the `GENIA+PubMed` parsing model:

```python
>>> from bllipparser import RerankingParser
>>> RerankingParser.fetch_and_load('GENIA+PubMed')
```

## Usage
Place reports in a single column csv `{reports_path}` where each row consists of a single report contained in quotes.

`python label.py --reports_path {reports_path}`

## Contributions
This repository builds upon the work of [NegBio](https://negbio.readthedocs.io/en/latest/).

This tool was developed by Jeremy Irvin, Pranav Rajpurkar, Michael Ko, Yifan Yu, and Silviana Ciurea-Ilcus.

## Citing
If you're using the CheXpert labeling tool, please cite:

INSERT CITATIONS
