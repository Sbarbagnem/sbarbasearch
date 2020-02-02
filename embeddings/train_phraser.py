import os
import time
import pickle
import logging
import argparse
import itertools
import numpy as np
from config import USERS_LIST
from gensim.models.phrases import Phrases, Phraser
from preprocess.tweet_preprocess import TweetPreprocess

logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)

args = argparse.ArgumentParser(
    description="Learn models to compute bigrams and trigrams from preprocessed query and users sentences. It uses the NPMI scoring function. It takes the users preprocessed sentences: if you want to preprocess first run python -m preprocess.preprocess"
)
args.add_argument(
    "--min-count",
    help="Take only words that has at least a min-count frequency",
    default=5,
    type=int,
)
args.add_argument(
    "--bigrams-thr",
    help="Threshold for which two words are a bigram",
    default=0.8,
    type=float,
)
args.add_argument(
    "--trigrams-thr",
    help="Threshold for which two words are a trigram",
    default=0.9,
    type=float,
)
args = args.parse_args()

if __name__ == "__main__":

    sentences = pickle.load(open(os.path.join("data", "query", "query.pkl"), "rb"))

    print("* LOADING USERS SENTENCES")
    for user in USERS_LIST:
        sentences.extend(
            pickle.load(open(os.path.join("data", "users", user + ".pkl"), "rb"))
        )

    print("* LEARNING BIGRAMS MODEL")
    bigram = Phraser(
        Phrases(
            sentences,
            scoring="npmi",
            min_count=args.min_count,
            threshold=args.bigrams_thr,
        )
    )

    print("* LEARNING BIGRAMS MODEL")
    trigram = Phraser(
        Phrases(
            bigram[sentences],
            scoring="npmi",
            min_count=args.min_count,
            threshold=args.trigrams_thr,
        )
    )

    bigram.save(os.path.join("data", "models", "bigram.pkl"))
    trigram.save(os.path.join("data", "models", "trigram.pkl"))

