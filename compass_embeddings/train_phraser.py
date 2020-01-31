import os
import time
import pickle
import logging
import itertools
import numpy as np
from config import USERS_LIST
from gensim.models.phrases import Phrases, Phraser
from preprocess.tweet_preprocess import TweetPreprocess

logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)

if __name__ == "__main__":

    sentences = pickle.load(open(os.path.join("data", "query", "query.pkl"), "rb"))

    for user in USERS_LIST:
        sentences.extend(
            pickle.load(open(os.path.join("data", "users", user + ".pkl"), "rb"))
        )

    # print("* PREPROCESSING QUERY TWEETS")
    # init = time.time()
    # # with mp.Pool(processes=cores-2) as pool:
    # #     query_tweets = pool.map(preprocess, query_tweets)
    # tweets = [
    #     TweetPreprocess.preprocess(tweet) for tweet in tqdm(query_tweets[:100])
    # ]
    # print("* DONE. EXPRIRED TIME: ", time.time() - init)

    # for user in USERS_LIST:
    #     print("* PREPROCESSING " + user + " TWEETS")
    #     init = time.time()
    #     user_tweets = [
    #         TweetPreprocess.preprocess(tweet) for tweet in tqdm(users_tweets[user])
    #     ]
    #     tweets.extend(user_tweets)
    #     print("* DONE. EXPRIRED TIME: ", time.time() - init)

    bigram = Phraser(Phrases(sentences, scoring="npmi", min_count=5, threshold=0.80))
    trigram = Phraser(
        Phrases(bigram[sentences], scoring="npmi", min_count=5, threshold=0.90)
    )
    bigram.save(os.path.join("data", "models", "bigram.pkl"))
    trigram.save(os.path.join("data", "models", "trigram.pkl"))

