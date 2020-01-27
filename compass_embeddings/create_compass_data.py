import os
import re
import json
import time
import html
import string
import itertools
import numpy as np
import multiprocessing as mp
from nltk import word_tokenize
from nltk.corpus import stopwords

english_stopwords = set(stopwords.words("english"))
uppercase_regex = re.compile(r"[a-z]+|[A-Z][a-z]+|\d+|[A-Z]+(?![a-z])")
url_regex = re.compile(r"https?:\/\/.*[\r\n]*")
hashtag_regex = re.compile(r"#([^\s#@]+)")


def split_by_capital_letter(m: re.Match):
    return " ".join(uppercase_regex.findall(m.group(1)))


def preprocess(doc):
    tokens = []
    yeah_tokens = []
    for tweet in doc:
        tweet = html.unescape(tweet)
        tweet = url_regex.sub("", tweet)
        tweet = hashtag_regex.sub(split_by_capital_letter, tweet)
        tokens = word_tokenize(tweet)
        for token in tokens:
            token = token.lower()
            if not (token == "rt" or token in english_stopwords or not token.isalnum()):
                yeah_tokens.append(token)
    if yeah_tokens != "":
        return " ".join(yeah_tokens)


if __name__ == "__main__":
    preprocess_data = True
    preprocess_method = "nltk"
    list_user = [
        "@MarcusRashford",
        "@AaronDonald97",
        "@GreenDay",
        "@MartinGarrix",
        "@EmmaWatson",
        "@VancityReynolds",
        "@elonmusk",
        "@IBM",
        "@realDonaldTrump",
        "@BorisJohnson",
        "@Yunus_Centre",
        "@JosephEStiglitz",
    ]

    query_tweets = json.load(open(os.path.join("..", "crawling_tweet", "tweet.json")))
    query_tweets = [query_tweet["text"] for query_tweet in query_tweets]

    user_tweets = {}
    for user in list_user:
        user_tweets[user] = json.load(
            open(os.path.join("..", "user_profile", "data", user + ".json"))
        )

    print("* PREPROCESSING QUERY TWEETS")
    init = time.time()
    # with mp.Pool(processes=cores-2) as pool:
    #     query_tweets = pool.map(preprocess, query_tweets)
    query_tweets = preprocess(query_tweets)
    print("* DONE. EXPRIRED TIME: ", time.time() - init)
    with open(os.path.join(".", "data", "query_tweets.txt"), "w+") as f:
        f.write(query_tweets)

    compass = query_tweets
    for user in list_user:
        print("* PREPROCESSING " + user + " TWEETS")
        init = time.time()
        user_tweet = preprocess(user_tweets[user])
        compass = compass + " " + user_tweet
        with open(os.path.join(".", "data", user + "_tweets.txt"), "w+") as f:
            f.write(user_tweet)
        print("* DONE. EXPRIRED TIME: ", time.time() - init)

    with open(os.path.join(".", "data", "compass.txt"), "w+") as f:
        f.write(compass)

