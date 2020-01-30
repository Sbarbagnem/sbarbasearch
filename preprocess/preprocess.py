import os
import json
import time
import pickle
import itertools
import numpy as np
import multiprocessing as mp
from pandas import pandas
from config import USERS_LIST
from pandarallel import pandarallel
from preprocess.tweet_preprocess import TweetPreprocess


def preprocess(return_preprocessed=False):
    pandarallel.initialize(nb_workers=mp.cpu_count() - 1, progress_bar=True)
    lengths = [0]
    load_filenames = [os.path.join("data", "query", "tweet.json")] + [
        os.path.join("data", "users", user + ".json") for user in USERS_LIST
    ]
    save_filenames = [os.path.join("data", "query", "tweet.pkl")] + [
        os.path.join("data", "users", user + ".pkl") for user in USERS_LIST
    ]
    print("* LOADING TWEETS")
    tweets = pandas.read_json(
        load_filenames[0], orient="columns", convert_axes=False, convert_dates=False,
    )[["text"]]
    lengths.append(len(tweets))
    for i in range(1, len(load_filenames)):
        print("* LOADING " + USERS_LIST[i - 1] + " TWEETS")
        users = (
            pandas.read_json(
                load_filenames[i],
                orient="index",
                convert_axes=False,
                convert_dates=False,
            )
            .reset_index(drop=True)
            .rename(columns={0: "text"})
        )
        lengths.append(len(users))
        tweets = pandas.concat([tweets, users], ignore_index=True)
    lengths = np.cumsum(lengths)
    init = time.time()
    print("* PREPROCESSING")
    tweets["text"] = tweets.parallel_apply(
        lambda x: TweetPreprocess.preprocess(x.text, return_list=False), axis=1
    )
    print("* ELAPSED TIME: {:.4f}".format(time.time() - init))
    if return_preprocessed:
        preprocessed = [0] * len(load_filenames)
    for i in range(1, len(lengths)):
        print("* SAVING PREPROCESSED TWEETS TO " + save_filenames[i - 1])
        chunk = tweets.iloc[lengths[i - 1] : lengths[i], :]
        values = chunk.text.apply(str.split).values.tolist()
        if return_preprocessed:
            preprocessed[i - 1] = values
        with open(save_filenames[i - 1], "wb+") as f:
            pickle.dump(values, f, protocol=pickle.HIGHEST_PROTOCOL)
            f.flush()
            f.close()
    if return_preprocessed:
        return preprocessed


if __name__ == "__main__":
    preprocess(return_preprocessed=False)

