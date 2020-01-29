import os
import json
import time
import itertools
import numpy as np
from tqdm import tqdm
from config import USERS_LIST
from preprocess.tweet_preprocess import TweetPreprocess

if __name__ == "__main__":

    load_query_txt = True
    if not load_query_txt:
        query_tweets = json.load(open(os.path.join("crawling_tweet", "tweet.json")))
        query_tweets = [query_tweet["text"] for query_tweet in query_tweets]

    users_tweets = {}
    for user in USERS_LIST:
        users_tweets[user] = json.load(
            open(os.path.join("user_profile", "data", user + ".json"))
        ).values()

    if not os.path.exists("./data"):
        os.makedirs("./data")

    if not load_query_txt:
        print("* PREPROCESSING QUERY TWEETS")
        init = time.time()
        # with mp.Pool(processes=cores-2) as pool:
        #     query_tweets = pool.map(preprocess, query_tweets)
        query_tweets = [
            TweetPreprocess.preprocess(tweet) for tweet in tqdm(query_tweets)
        ]
        print("* DONE. EXPRIRED TIME: ", time.time() - init)
        query_tweets = " ".join(list(itertools.chain(*query_tweets)))
        with open(
            os.path.join("compass_embeddings", "data", "query_tweets.txt"), "w+"
        ) as f:
            f.write(query_tweets)
    else:
        query_tweets = " ".join(
            np.loadtxt(
                os.path.join("compass_embeddings", "data", "query_tweets.txt"),
                dtype="str",
            )
        )

    compass = query_tweets
    for user in USERS_LIST:
        print("* PREPROCESSING " + user + " TWEETS")
        init = time.time()
        user_tweets = [
            TweetPreprocess.preprocess(tweet) for tweet in tqdm(users_tweets[user])
        ]
        user_tweets = " ".join(list(itertools.chain(*user_tweets)))
        compass = compass + " " + user_tweets
        with open(
            os.path.join("compass_embeddings", "data", user + "_tweets.txt"), "w+"
        ) as f:
            f.write(user_tweets)
        print("* DONE. EXPRIRED TIME: ", time.time() - init)

    with open(os.path.join("compass_embeddings", "data", "compass.txt"), "w+") as f:
        f.write(compass)

