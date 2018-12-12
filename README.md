# chexpert-labeler
CheXpert NLP tool to extract observations from radiology reports.

## Prerequisites
1. Clone the [NegBio repository](https://github.com/ncbi-nlp/NegBio):
    
    `git clone git@github.com:ncbi-nlp/NegBio.git`

2. Add the NegBio directory to your `PYTHONPATH`:
    
    `export PYTHONPATH={path to negbio directory}:$PYTHONPATH`

3. Make the virtual environment:
    
    `conda env create -f environment.yml`

4. Install NLTK data:
    
    `python -m nltk.downloader universal_tagset punkt wordnet`

5. Download the `GENIA+PubMed` parsing model:

```python
>>> from bllipparser import RerankingParser
>>> RerankingParser.fetch_and_load('GENIA+PubMed')
```

## Usage
Place reports in a headerless, single column csv `{reports_path}`. Each report must be contained in quotes if (1) it contains a comma or (2) it spans multiple lines. See [sample_reports.csv](https://raw.githubusercontent.com/stanfordmlgroup/chexpert-labeler/cleanup-and-port/sample_reports.csv?token=AG0zZhDd8WNzT1f85KtdyvJmoirEizdkks5cGravwA%3D%3D) for an example. 

`python label.py --reports_path {reports_path}`

## Contributions
This repository builds upon the work of [NegBio](https://negbio.readthedocs.io/en/latest/).

This tool was developed by Jeremy Irvin, Pranav Rajpurkar, Michael Ko, Yifan Yu, and Silviana Ciurea-Ilcus.

## Citing
If you're using the CheXpert labeling tool, please cite:

INSERT CITATIONS
