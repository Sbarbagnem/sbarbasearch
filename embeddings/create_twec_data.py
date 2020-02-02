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
    description="Create TWEC data: compass.txt, query.txt and a .txt for every user. It takes the users preprocessed sentences: if you want to preprocess first run python -m preprocess.preprocess"
)
args.add_argument(
    "-b", "--bigrams", help="Whether to compute bigrams", action="store_true",
)
args.add_argument(
    "-t", "--trigrams", help="Whether to compute trigrams", action="store_true",
)
args = args.parse_args()

if __name__ == "__main__":

    compute_n_grams = True

    if args.bigrams:
        bigram = Phraser.load(os.path.join("data", "models", "bigram.pkl"))
    if args.trigrams:
        trigram = Phraser.load(os.path.join("data", "models", "trigram.pkl"))

    print("* LOADING QUERY SENTENCES")
    sentences = pickle.load(open(os.path.join("data", "query", "query.pkl"), "rb"))
    if args.bigrams or args.trigrams:
        print("* COMPUTING BIGRAMS/TRIGRAMS")
        if args.bigrams:
            sentences = bigram[sentences]
        if args.trigrams:
            sentences = trigram[sentences]

    sentences = " ".join(list(itertools.chain(*sentences)))
    with open(os.path.join("data", "twec", "query.txt"), "w+") as f:
        print("* SAVING QUERY TXT")
        f.write(sentences)

    for user in USERS_LIST:
        print("* LOADING " + user + " SENTENCES")
        user_sentences = pickle.load(
            open(os.path.join("data", "users", user + ".pkl"), "rb")
        )
        if args.bigrams or args.trigrams:
            print("* COMPUTING BIGRAMS/TRIGRAMS")
            if args.bigrams:
                user_sentences = bigram[user_sentences]
            if args.trigrams:
                user_sentences = trigram[user_sentences]

        user_sentences = " ".join(list(itertools.chain(*user_sentences)))
        sentences = sentences + " " + user_sentences
        with open(os.path.join("data", "twec", user + ".txt"), "w+") as f:
            print("* SAVING " + user + " TXT")
            f.write(user_sentences)

    with open(os.path.join("data", "twec", "compass.txt"), "w+") as f:
        print("* SAVING COMPASS TXT")
        f.write(sentences)
