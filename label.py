"""Entry-point script to label radiology reports."""
import pandas as pd

from args import ArgParser
from loader import Loader
from stages import Extractor, Classifier, Aggregator
from constants import *


def label(args):
    """Label the provided report(s)."""

    # Load the reports
    loader = Loader(args.reports_path, args.extract_impression)

    extractor = Extractor(args.mention_phrases_dir,
                          args.unmention_phrases_dir,
                          verbose=args.verbose)
    classifier = Classifier(args.pre_negation_uncertainty_path,
                            args.negation_path,
                            args.post_negation_uncertainty_path,
                            verbose=args.verbose)
    aggregator = Aggregator(CATEGORIES,
                            verbose=args.verbose)

    # Extract observation mentions in place.
    extractor.extract(loader.collection)
    # Classify mentions in place.
    classifier.classify(loader.collection)
    # Aggregate mentions to obtain one set of labels for each report.
    labels = aggregator.aggregate(loader.collection)

    labeled_reports = pd.DataFrame({REPORTS: loader.reports})
    for index, category in enumerate(CATEGORIES):
        labeled_reports[category] = labels[:, index]

    if args.verbose:
        print(f"Writing reports and labels to {args.output_path}.")
    labeled_reports[[REPORTS] + CATEGORIES].to_csv(args.output_path,
                                                   index=False)


if __name__ == "__main__":
    parser = ArgParser()
    label(parser.parse_args())
