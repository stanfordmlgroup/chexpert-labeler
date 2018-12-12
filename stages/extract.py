"""Define observation extractor class."""
import re
import itertools
from collections import defaultdict
from tqdm import tqdm
from constants import *

import bioc


class Extractor(object):
    """Extract observations from impression sections of reports."""
    def __init__(self, mention_phrases_dir, unmention_phrases_dir,
                 verbose=False):
        self.verbose = verbose
        self.observation2mention_phrases\
            = self.load_phrases(mention_phrases_dir, "mention")
        self.observation2unmention_phrases\
            = self.load_phrases(unmention_phrases_dir, "unmention")
        self.add_unmention_phrases()

    def load_phrases(self, phrases_dir, phrases_type):
        """Read in map from observations to phrases for matching."""
        observation2phrases = defaultdict(list)
        for phrases_path in phrases_dir.glob("*.txt"):
            with phrases_path.open() as f:
                for line in f:
                    phrase = line.strip().replace("_", " ")
                    observation = phrases_path.stem.replace("_", " ").title()
                    if line:
                        observation2phrases[observation].append(phrase)

        if self.verbose:
            print(f"Loading {phrases_type} phrases for "
                  f"{len(observation2phrases)} observations.")

        return observation2phrases

    def add_unmention_phrases(self):
        cardiomegaly_mentions\
            = self.observation2mention_phrases[CARDIOMEGALY]
        enlarged_cardiom_mentions\
            = self.observation2mention_phrases[ENLARGED_CARDIOMEDIASTINUM]
        positional_phrases = (["over the", "overly the", "in the"],
                              ["", " superior", " left", " right"])
        positional_unmentions = [e1 + e2
                                 for e1 in positional_phrases[0]
                                 for e2 in positional_phrases[1]]
        cardiomegaly_unmentions = [e1 + " " + e2.replace("the ", "")
                                   for e1 in positional_unmentions
                                   for e2 in cardiomegaly_mentions
                                   if e2 not in ["cardiomegaly",
                                                 "cardiac enlargement"]]
        enlarged_cardiomediastinum_unmentions\
            = [e1 + " " + e2
               for e1 in positional_unmentions
               for e2 in enlarged_cardiom_mentions]

        self.observation2unmention_phrases[CARDIOMEGALY]\
            = cardiomegaly_unmentions
        self.observation2unmention_phrases[ENLARGED_CARDIOMEDIASTINUM]\
            = enlarged_cardiomediastinum_unmentions

    def overlaps_with_unmention(self, sentence, observation, start, end):
        """Return True if a given match overlaps with an unmention phrase."""
        unmention_overlap = False
        unmention_list = self.observation2unmention_phrases.get(observation,
                                                                [])
        for unmention in unmention_list:
            unmention_matches = re.finditer(unmention, sentence.text)
            for unmention_match in unmention_matches:
                unmention_start, unmention_end = unmention_match.span(0)
                if start < unmention_end and end > unmention_start:
                    unmention_overlap = True
                    break  # break early if overlap is found
            if unmention_overlap:
                break  # break early if overlap is found

        return unmention_overlap

    def add_match(self, impression, sentence, ann_index, phrase,
                  observation, start, end):
        """Add the match data and metadata to the impression object
        in place."""
        annotation = bioc.BioCAnnotation()
        annotation.id = ann_index
        annotation.infons['CUI'] = None
        annotation.infons['semtype'] = None
        annotation.infons['term'] = phrase
        annotation.infons[OBSERVATION] = observation
        annotation.infons['annotator'] = 'Phrase'
        length = end - start
        annotation.add_location(bioc.BioCLocation(sentence.offset + start,
                                                  length))
        annotation.text = sentence.text[start:start+length]

        impression.annotations.append(annotation)

    def extract(self, collection):
        """Extract the observations in each report.

        Args:
            collection (BioCCollection): Impression passages of each report.

        Return:
            extracted_mentions
        """

        # The BioCCollection consists of a series of documents.
        # Each document is a report (just the Impression section
        # of the report.)
        documents = collection.documents
        if self.verbose:
            print("Extracting mentions...")
            documents = tqdm(documents)
        for document in documents:
            # Get the Impression section.
            impression = document.passages[0]
            annotation_index = itertools.count(len(impression.annotations))

            for sentence in impression.sentences:
                obs_phrases = self.observation2mention_phrases.items()
                for observation, phrases in obs_phrases:
                    for phrase in phrases:
                        matches = re.finditer(phrase, sentence.text)
                        for match in matches:
                            start, end = match.span(0)

                            if self.overlaps_with_unmention(sentence,
                                                            observation,
                                                            start,
                                                            end):
                                continue

                            self.add_match(impression,
                                           sentence,
                                           str(next(annotation_index)),
                                           phrase,
                                           observation,
                                           start,
                                           end)
