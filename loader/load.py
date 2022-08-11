"""Define report loader class."""
import warnings
import re
import bioc
import pandas as pd
from negbio.pipeline import text2bioc, ssplit, section_split

from constants import *


class Loader(object):
    """Report impression loader."""
    def __init__(self, reports_path, sections_to_extract):
        self.reports_path = reports_path
        self.sections_to_extract = sections_to_extract
        self.punctuation_spacer = str.maketrans({key: f"{key} "
                                                 for key in ".,"})
        self.splitter = ssplit.NegBioSSplitter(newline=False)

    def load(self):
        """Load and clean the reports."""
        collection = bioc.BioCCollection()
        reports = pd.read_csv(self.reports_path,
                              header=None,
                              names=[REPORTS])[REPORTS].tolist()

        for i, report in enumerate(reports):
            clean_report = self.clean(report)
            document = text2bioc.text2document(str(i), clean_report)

            if self.sections_to_extract:
                document = self.extract_sections(document)

            split_document = self.splitter.split_doc(document)

            assert len(split_document.passages) == 1,\
                ('Each document must be given as a single passage.')

            collection.add_document(split_document)

        self.reports = reports
        self.collection = collection

    def extract_sections(self, document):
        """Extract the Impression section from a Bioc Document."""
        split_document = section_split.split_document(document)
        passages = []
        for i, passage in enumerate(split_document.passages):
            if 'title' in passage.infons:
                if (passage.infons['title'] in self.sections_to_extract and
                    len(split_document.passages) > i+1):
                    next_passage = split_document.passages[i+1]
                    if 'title' not in next_passage.infons:
                        passages.append(next_passage)
        
        if passages:
            extracted_passages = bioc.BioCPassage()
            extracted_passages.offset = findings_impression_passages[0].offset
            extracted_passages.text = ' '.join(map(lambda x: x.text, passages))
            split_document.passages = [extracted_passages]
            return split_document
        else:
            warnings.warn('Loader found document containing none of the ' + 
                          'provided sections to extract. Returning original ' + 
                          'document.')
            return document

    def clean(self, report):
        """Clean the report text."""
        lower_report = report.lower()
        # Change `and/or` to `or`.
        corrected_report = re.sub('and/or',
                                  'or',
                                  lower_report)
        # Change any `XXX/YYY` to `XXX or YYY`.
        corrected_report = re.sub('(?<=[a-zA-Z])/(?=[a-zA-Z])',
                                  ' or ',
                                  corrected_report)
        # Clean double periods
        clean_report = corrected_report.replace("..", ".")
        # Insert space after commas and periods.
        clean_report = clean_report.translate(self.punctuation_spacer)
        # Convert any multi white spaces to single white spaces.
        clean_report = ' '.join(clean_report.split())
        # Remove empty sentences
        clean_report = re.sub(r'\.\s+\.', '.', clean_report)

        return clean_report
