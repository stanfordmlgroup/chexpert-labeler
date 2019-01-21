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
Place reports in a headerless, single column csv `{reports_path}`. Each report must be contained in quotes if (1) it contains a comma or (2) it spans multiple lines. See [sample_reports.csv](https://raw.githubusercontent.com/stanfordmlgroup/chexpert-labeler/master/sample_reports.csv?token=AG0zZp8rZhV4o7llgkL6lhGzEt8CoSQbks5cGsIBwA%3D%3D) for an example. 

`python label.py --reports_path {reports_path}`

Run `python label.py --help` for descriptions of all of the command-line arguments.

## Contributions
This repository builds upon the work of [NegBio](https://negbio.readthedocs.io/en/latest/).

This tool was developed by Jeremy Irvin, Pranav Rajpurkar, Michael Ko, Yifan Yu, and Silviana Ciurea-Ilcus.

## Citing
If you're using the CheXpert labeling tool, please cite:

Irvin, Jeremy, et al. "CheXpert: A large chest radiograph dataset with uncertainty labels and expert comparison." Thirty-Third AAAI Conference on Artificial Intelligence. 2019.

```
@inproceedings{irvin2019chexpert,
  title={CheXpert: A large chest radiograph dataset with uncertainty labels and expert comparison},
  author={Irvin, Jeremy and Rajpurkar, Pranav and Ko, Michael and Yu, Yifan and Ciurea-Ilcus, Silviana and Chute, Chris and Marklund, Henrik and Haghgoo, Behzad and Ball, Robyn and Shpanskaya, Katie and others},
  booktitle={Thirty-Third AAAI Conference on Artificial Intelligence},
  year={2019}
}
```
