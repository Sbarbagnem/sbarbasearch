import os
import re
import json
import time
import html
import string
import itertools
import numpy as np
import multiprocessing as mp
from tqdm import tqdm
from nltk import word_tokenize
from nltk.corpus import stopwords
from config import USERS_LIST

english_stopwords = set(stopwords.words("english"))
uppercase_regex = re.compile(r"[a-z]+|[A-Z][a-z]+|\d+|[A-Z]+(?![a-z])")
url_regex = re.compile(
    # u"^"
    # protocol identifier
    u"(?:(?:(?:https?|ftp):)?//)"
    # user:pass authentication
    u"(?:\S+(?::\S*)?@)?" u"(?:"
    # IP address exclusion
    # private & local networks
    u"(?!(?:10|127)(?:\.\d{1,3}){3})"
    u"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    u"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    u"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    u"|"
    # host & domain names, may end with dot
    # can be replaced by a shortest alternative
    # u"(?![-_])(?:[-\w\u00a1-\uffff]{0,63}[^-_]\.)+"
    # u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
    # # domain name
    # u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
    u"(?:"
    u"(?:"
    u"[a-z0-9\u00a1-\uffff]"
    u"[a-z0-9\u00a1-\uffff_-]{0,62}"
    u")?"
    u"[a-z0-9\u00a1-\uffff]\."
    u")+"
    # TLD identifier name, may end with dot
    u"(?:[a-z\u00a1-\uffff]{2,}\.?)" u")"
    # port number (optional)
    u"(?::\d{2,5})?"
    # resource path (optional)
    u"(?:[/?#]\S*)?"
    # u"$",
    ,
    re.UNICODE | re.I | re.MULTILINE,
)
hashtag_regex = re.compile(r"#([^\s#@]+)", flags=re.MULTILINE)
non_alphanum_regex = re.compile(r'\W+')  # Match everything that is not contained in [a-zA-Z0-9_]


def split_by_capital_letter(m: re.Match):
    return " ".join(uppercase_regex.findall(m.group(1)))


def preprocess(doc, verbose=False):
    tokens = []
    yeah_tokens = []
    for tweet in tqdm(doc):
        if verbose:
            print('* BEFORE')
            print(tweet)
        tweet = html.unescape(html.unescape(tweet))
        tweet = url_regex.sub("", tweet)
        tweet = hashtag_regex.sub(split_by_capital_letter, tweet)
        if verbose:
            print('* AFTER REGEXES PREPROCESSING')
            print(tweet)
        tokens = word_tokenize(tweet)
        if verbose:
            print('* AFTER TOKENIZATION')
            print(tokens)
        for token in tokens:
            token = token.lower()
            if not (token == "rt" or token in english_stopwords or non_alphanum_regex.match(token)):
                yeah_tokens.append(token)
    return " ".join(yeah_tokens)


if __name__ == "__main__":
    preprocess_data = True
    preprocess_method = "nltk"

    query_tweets = json.load(open(os.path.join("..", "crawling_tweet", "tweet.json")))
    query_tweets = [query_tweet["text"] for query_tweet in query_tweets]

    user_tweets = {}
    for user in USERS_LIST:
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
    for user in USERS_LIST:
        print("* PREPROCESSING " + user + " TWEETS")
        init = time.time()
        user_tweet = preprocess(user_tweets[user])
        compass = compass + " " + user_tweet
        with open(os.path.join(".", "data", user + "_tweets.txt"), "w+") as f:
            f.write(user_tweet)
        print("* DONE. EXPRIRED TIME: ", time.time() - init)

    with open(os.path.join(".", "data", "compass.txt"), "w+") as f:
        f.write(compass)

