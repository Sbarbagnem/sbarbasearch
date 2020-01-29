import os
import json
import time
import itertools
import numpy as np
from tqdm import tqdm
from config import USERS_LIST
from gensim.models.phrases import Phrases, Phraser
from preprocess.tweet_preprocess import TweetPreprocess

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

if __name__ == "__main__":

    query_tweets = json.load(open(os.path.join("crawling_tweet", "tweet.json")))
    query_tweets = [query_tweet["text"] for query_tweet in query_tweets]

    users_tweets = {}
    for user in USERS_LIST:
        users_tweets[user] = json.load(
            open(os.path.join("user_profile", "data", user + ".json"))
        ).values()

    print("* PREPROCESSING QUERY TWEETS")
    init = time.time()
    # with mp.Pool(processes=cores-2) as pool:
    #     query_tweets = pool.map(preprocess, query_tweets)
    tweets = [
        TweetPreprocess.preprocess(tweet) for tweet in tqdm(query_tweets[:100])
    ]
    print("* DONE. EXPRIRED TIME: ", time.time() - init)

    for user in USERS_LIST:
        print("* PREPROCESSING " + user + " TWEETS")
        init = time.time()
        user_tweets = [
            TweetPreprocess.preprocess(tweet) for tweet in tqdm(users_tweets[user])
        ]
        tweets.extend(user_tweets)
        print("* DONE. EXPRIRED TIME: ", time.time() - init)
    
    bigram = Phraser(Phrases(tweets, scoring='npmi', min_count=5, threshold=0.80))
    trigram = Phraser(Phrases(bigram[tweets], scoring='npmi', min_count=5, threshold=0.90))
    bigram.save(os.path.join("compass_embeddings", "model", "bigram.pkl"))
    trigram.save(os.path.join("compass_embeddings", "model", "trigram.pkl"))
    

