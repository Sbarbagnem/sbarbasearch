import os
import time
import pickle
import itertools
import numpy as np
from config import USERS_LIST
from gensim.models.phrases import Phrases, Phraser
from preprocess.tweet_preprocess import TweetPreprocess

if __name__ == "__main__":

    compute_n_grams = True

    if compute_n_grams:
        bigram = Phraser.load(os.path.join("data", "models", "bigram.pkl"))
        trigram = Phraser.load(os.path.join("data", "models", "trigram.pkl"))

    sentences = pickle.load(open(os.path.join("data", "query", "tweet.pkl"), "rb"))
    if compute_n_grams:
        sentences = trigram[bigram[sentences]]
    sentences = " ".join(list(itertools.chain(*sentences)))
    with open(os.path.join("data", "twec", "tweets.txt"), "w+") as f:
        f.write(sentences)

    for user in USERS_LIST:
        user_sentences = pickle.load(
            open(os.path.join("data", "users", user + ".pkl"), "rb")
        )
        if compute_n_grams:
            user_sentences = trigram[bigram[user_sentences]]
        user_sentences = " ".join(list(itertools.chain(*user_sentences)))
        sentences = sentences + " " + user_sentences
        with open(os.path.join("data", "twec", user + ".txt"), "w+") as f:
            f.write(user_sentences)

    with open(os.path.join("data", "twec", "compass.txt"), "w+") as f:
        f.write(sentences)

