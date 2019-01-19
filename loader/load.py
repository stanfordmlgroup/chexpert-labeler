"""Define report loader class."""
import re
import bioc
import pandas as pd
from negbio.pipeline import text2bioc, ssplit

from constants import *


class Loader(object):
    """Report impression loader."""
    def __init__(self, reports_path, extract_impression=False):
        self.reports_path = reports_path
        self.extract_impression = extract_impression
        self.punctuation_spacer = str.maketrans({key: f"{key} "
                                                 for key in ".,"})
        self.splitter = ssplit.NltkSSplitter(newline=False)

    def load(self):
        """Load and clean the reports."""
        collection = bioc.BioCCollection()
        reports = pd.read_csv(self.reports_path,
                              header=None,
                              names=[REPORTS])[REPORTS].tolist()

        for i, report in enumerate(reports):
            clean_report = self.clean(report)
            document = text2bioc.text2document(str(i), clean_report,
                                               split_document=self.extract_impression)
            if self.extract_impression:
                self.extract_impression_from_passages(document)

            split_document = ssplit.ssplit(document, self.splitter)

            assert len(split_document.passages) == 1,\
                ('Each document must have a single passage, ' +
                 'the Impression section.')

            collection.add_document(split_document)

        self.reports = reports
        self.collection = collection

    def extract_impression_from_passages(self, document):
        """Extract the Impression section from a Bioc Document."""
        document.passages = [passage for passage in document.passages
                             if passage.infons['title'] == "impression"]

        assert len(document.passages) <= 1,\
            (f"The document contains {len(document.passages)} impression " +
             "passages.")

        assert len(document.passages) >= 1,\
            "The document contains no explicit impression passage."

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

        return clean_report
