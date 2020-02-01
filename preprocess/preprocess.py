import os
import json
import time
import pickle
import argparse
import itertools
import numpy as np
import multiprocessing as mp
from pandas import pandas
from config import USERS_LIST
from pandarallel import pandarallel
from preprocess.tweet_preprocess import TweetPreprocess


def preprocess(save=True, return_preprocessed=False, workers=mp.cpu_count() - 1):
    pandarallel.initialize(nb_workers=workers, progress_bar=True)
    lengths = [0]
    load_filenames = [os.path.join("data", "query", "query.json")] + [
        os.path.join("data", "users", user + ".json") for user in USERS_LIST
    ]
    save_filenames = [os.path.join("data", "query", "query.pkl")] + [
        os.path.join("data", "users", user + ".pkl") for user in USERS_LIST
    ]
    print("* LOADING QUERY TWEETS")
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
        if save:
            with open(save_filenames[i - 1], "wb+") as f:
                pickle.dump(values, f, protocol=pickle.HIGHEST_PROTOCOL)
                f.flush()
                f.close()
    if return_preprocessed:
        return preprocessed


def preprocess_memory_oriented(
    save=True, return_preprocessed=False, workers=mp.cpu_count() - 1
):
    pandarallel.initialize(nb_workers=workers, progress_bar=True)

    load_filenames = [os.path.join("data", "query", "query.json")] + [
        os.path.join("data", "users", user + ".json") for user in USERS_LIST
    ]
    save_filenames = [os.path.join("data", "query", "query.pkl")] + [
        os.path.join("data", "users", user + ".pkl") for user in USERS_LIST
    ]
    if return_preprocessed:
        preprocessed = [0] * len(load_filenames)

    for i in range(len(load_filenames)):
        if i == 0:
            print("* LOADING QUERY TWEETS")
            tweets = pandas.read_json(
                load_filenames[i],
                orient="columns",
                convert_axes=False,
                convert_dates=False,
            )[["text"]]
        else:
            print("* LOADING " + USERS_LIST[i - 1] + " TWEETS")
            tweets = (
                pandas.read_json(
                    load_filenames[i],
                    orient="index",
                    convert_axes=False,
                    convert_dates=False,
                )
                .reset_index(drop=True)
                .rename(columns={0: "text"})
            )

        print("* PREPROCESSING")
        init = time.time()
        tweets["text"] = tweets.parallel_apply(
            lambda x: TweetPreprocess.preprocess(x.text, return_list=False), axis=1
        )
        print("* ELAPSED TIME: {:.4f}".format(time.time() - init))

        values = tweets.text.apply(str.split).values.tolist()
        if return_preprocessed:
            preprocessed[i] = values
        if save:
            print("* SAVING PREPROCESSED TWEETS TO " + save_filenames[i])
            with open(save_filenames[i], "wb+") as f:
                pickle.dump(values, f, protocol=pickle.HIGHEST_PROTOCOL)
                f.flush()
                f.close()
    if return_preprocessed:
        return preprocessed


args = argparse.ArgumentParser()
args.add_argument(
    "--mem-oriented",
    help="Whether to preprocess files in a memory-oriented manner",
    action="store_true",
)
args.add_argument(
    "-s",
    "--save",
    help="Whether to save the preprocessed files. If true, it saves files as list of lists in a pickle format. It saves in the same dir where the json are",
    action="store_true",
)
args.add_argument(
    "-w",
    "--workers",
    help="How many cores to use during the preprocessing. Default system-cores - 1",
    default=mp.cpu_count() - 1,
    type=int
)
args = args.parse_args()

if __name__ == "__main__":
    save = args.save
    if args.mem_oriented:
        preprocess_memory_oriented(save=save, return_preprocessed=False, workers=args.workers)
    else:
        preprocess(save=save, return_preprocessed=False, workers=args.workers)

