"""Define mention aggregator class."""
import numpy as np
from tqdm import tqdm

from constants import *


class Aggregator(object):
    """Aggregate mentions of observations from radiology reports."""
    def __init__(self, categories, verbose=False):
        self.categories = categories

        self.verbose = verbose

    def dict_to_vec(self, d):
        """
        Convert a dictionary of the form

        {cardiomegaly: [1],
         opacity: [u, 1],
         fracture: [0]}

        into a vector of the form

        [np.nan, np.nan, 1, u, np.nan, ..., 0, np.nan]
        """
        vec = []
        for category in self.categories:
            # There was a mention of the category.
            if category in d:
                label_list = d[category]
                # Only one label, no conflicts.
                if len(label_list) == 1:
                    vec.append(label_list[0])
                # Multiple labels.
                else:
                    # Case 1. There is 0 and u.
                    if 0 in label_list and -1 in label_list:
                        vec.append(-1)
                    # Case 2. There is 0 and 1.
                    elif 0 in label_list and 1 in label_list:
                        vec.append(1)
                    # Case 3. There is u and 1.
                    elif -1 in label_list and 1 in label_list:
                        vec.append(1)
                    # Case 4. All labels are the same.
                    else:
                        vec.append(label_list[0])

            # No mention of the category
            else:
                vec.append(np.nan)

        return vec

    def aggregate(self, collection):
        labels = []
        documents = collection.documents
        if self.verbose:
            print("Aggregating mentions...")
            documents = tqdm(documents)
        for document in documents:
            label_dict = {}
            impression_passage = document.passages[0]
            no_finding = True
            for annotation in impression_passage.annotations:
                category = annotation.infons[OBSERVATION]

                if NEGATION in annotation.infons:
                    label = 0
                elif UNCERTAINTY in annotation.infons:
                    label = -1
                else:
                    label = 1

                # If at least one non-support category has a -1 (u) or 1
                # label, there was a finding
                if category != SUPPORT_DEVICES and label in [-1, 1]:
                    no_finding = False

                # Don't add any labels for No Finding
                if category == NO_FINDING:
                    continue

                # add exception for 'chf' and 'heart failure'
                if ((label == 1 or label == -1) and
                    (annotation.text == 'chf' or
                     annotation.text == 'heart failure')):
                    if CARDIOMEGALY not in label_dict:
                        label_dict[CARDIOMEGALY] = [-1]
                    else:
                        label_dict[CARDIOMEGALY].append(-1)

                if category not in label_dict:
                    label_dict[category] = [label]
                else:
                    label_dict[category].append(label)

            if no_finding:
                label_dict[NO_FINDING] = [1]

            label_vec = self.dict_to_vec(label_dict)

            labels.append(label_vec)

        return np.array(labels)
