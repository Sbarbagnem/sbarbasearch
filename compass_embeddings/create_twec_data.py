import os
import re
import json
import time
import html
import string
import itertools
import contractions
import numpy as np
from tqdm import tqdm
import multiprocessing as mp
from config import USERS_LIST
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize.casual import TweetTokenizer
from preprocess.tweet_preprocess import TweetPreprocess

english_stopwords = set(stopwords.words("english"))
non_alphanum_regex = re.compile(
    r"\W+"
)  # Match everything that is not contained in [a-zA-Z0-9_]


def preprocess(doc, tokenizer='twitter', verbose=False):
    tokens = []
    yeah_tokens = []
    tokenizer = word_tokenize
    if tokenizer == 'twitter':
        tokenizer = TweetTokenizer().tokenize
    for tweet in tqdm(doc):
        if verbose:
            print("* BEFORE")
            print(tweet)
        preprocessor.text = html.unescape(html.unescape(tweet))
        # tweet = html.unescape(html.unescape(tweet))
        preprocessor.remove_urls(full=True)
        # tweet = url_regex.sub("", tweet)
        preprocessor.remove_hashtags(split_capital_letter=True)
        # tweet = hashtag_regex.sub(split_by_capital_letter, tweet)
        preprocessor.remove_mentions()
        preprocessor.remove_emojis()
        tweet = contractions.fix(preprocessor.text)
        if verbose:
            print("* AFTER REGEXES PREPROCESSING")
            print(tweet)
        tokens = tokenizer(tweet)
        if verbose:
            print("* AFTER TOKENIZATION")
            print(tokens)
        for token in tokens:
            token = token.lower()
            if not (
                token == "rt"
                or token in english_stopwords
                or non_alphanum_regex.match(token)
                or (token.isalpha() and len(token) < 2)
            ):
                yeah_tokens.append(token)
    return " ".join(yeah_tokens)


if __name__ == "__main__":
    tweet_tokenizer = TweetTokenizer()
    preprocessor = TweetPreprocess(text="")

    query_tweets = json.load(open(os.path.join("crawling_tweet", "tweet.json")))
    query_tweets = [query_tweet["text"] for query_tweet in query_tweets]

    user_tweets = {}
    for user in USERS_LIST:
        user_tweets[user] = json.load(
            open(os.path.join("user_profile", "data", user + ".json"))
        ).values()

    if not os.path.exists('./data'):
        os.makedirs('./data')

    print("* PREPROCESSING QUERY TWEETS")
    init = time.time()
    # with mp.Pool(processes=cores-2) as pool:
    #     query_tweets = pool.map(preprocess, query_tweets)
    query_tweets = preprocess(query_tweets, verbose=False)
    print("* DONE. EXPRIRED TIME: ", time.time() - init)
    with open(
        os.path.join("compass_embeddings", "data", "query_tweets.txt"), "w+"
    ) as f:
        f.write(query_tweets)

    compass = query_tweets
    for user in USERS_LIST:
        print("* PREPROCESSING " + user + " TWEETS")
        init = time.time()
        user_tweet = preprocess(user_tweets[user])
        compass = compass + " " + user_tweet
        with open(
            os.path.join("compass_embeddings", "data", user + "_tweets.txt"), "w+"
        ) as f:
            f.write(user_tweet)
        print("* DONE. EXPRIRED TIME: ", time.time() - init)

    with open(os.path.join("compass_embeddings", "data", "compass.txt"), "w+") as f:
        f.write(compass)

