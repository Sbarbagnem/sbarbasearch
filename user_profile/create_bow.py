import os
import time
import json
import pickle
import argparse
import numpy as np
from config import USERS_LIST
from gensim.models.phrases import Phraser
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

args = argparse.ArgumentParser(
    description="Create BagOfWords for every users using TF-IDF. It takes the users preprocessed sentences: if you want to preprocess first run python -m preprocess.preprocess"
)
args.add_argument(
    "-b", "--bigrams", help="Whether to compute bigrams", action="store_true",
)
args.add_argument(
    "-t", "--trigrams", help="Whether to compute trigrams", action="store_true",
)
args.add_argument(
    "--top-n",
    help="Take the first n element of the ordered TF-IDF matrix",
    default=10,
    type=int,
)
args = args.parse_args()

if __name__ == "__main__":

    bow = {}
    compute_n_grams = True

    if args.bigrams:
        bigram = Phraser.load(os.path.join("data", "models", "bigram.pkl"))
    if args.trigrams:
        trigram = Phraser.load(os.path.join("data", "models", "trigram.pkl"))

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
        user_sentences = map(lambda sentence: " ".join(sentence), user_sentences)
        tf = CountVectorizer(
            lowercase=False,
            analyzer="word",
            tokenizer=lambda x: x.split(),
            token_pattern=None,
        )
        print("* TF")
        X = tf.fit_transform(user_sentences)
        freqs = zip(tf.get_feature_names(), X.sum(axis=0).tolist()[0])
        freqs = sorted(freqs, key=lambda x: -x[1])
        bow[user] = [freqs[i][0] for i in range(args.top_n)]

    opath = os.path.join("data", "users", "bow_tf.json")
    with open(opath, "w") as f:
        json.dump(bow, f)
