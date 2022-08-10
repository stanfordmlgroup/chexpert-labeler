"""Define argument parser class."""
import argparse
from pathlib import Path


class ArgParser(object):
    """Argument parser for label.py"""
    def __init__(self):
        """Initialize argument parser."""
        parser = argparse.ArgumentParser()

        # Input report parameters.
        parser.add_argument('--reports_path',
                            required=True,
                            help='Path to file with radiology reports.')
        parser.add_argument('--sections_to_extract',
                            nargs='+',
                            default=['impression'],
                            help='Titles of the sections to extract from ' +
                                 'each report.')

        # Phrases
        parser.add_argument('--mention_phrases_dir',
                            default='phrases/mention',
                            help='Directory containing mention phrases for ' +
                                 'each observation.')
        parser.add_argument('--unmention_phrases_dir',
                            default='phrases/unmention',
                            help='Directory containing unmention phrases ' +
                                 'for each observation.')

        # Rules
        parser.add_argument('--pre_negation_uncertainty_path',
                            default='patterns/pre_negation_uncertainty.txt',
                            help='Path to pre-negation uncertainty rules.')
        parser.add_argument('--negation_path',
                            default='patterns/negation.txt',
                            help='Path to negation rules.')
        parser.add_argument('--post_negation_uncertainty_path',
                            default='patterns/post_negation_uncertainty.txt',
                            help='Path to post-negation uncertainty rules.')

        # Output parameters.
        parser.add_argument('--output_path',
                            default='labeled_reports.csv',
                            help='Output path to write labels to.')

        # Misc.
        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            help='Print progress to stdout.')

        self.parser = parser

    def parse_args(self):
        """Parse and validate the supplied arguments."""
        args = self.parser.parse_args()

        args.reports_path = Path(args.reports_path)
        args.mention_phrases_dir = Path(args.mention_phrases_dir)
        args.unmention_phrases_dir = Path(args.unmention_phrases_dir)
        args.output_path = Path(args.output_path)

        return args
