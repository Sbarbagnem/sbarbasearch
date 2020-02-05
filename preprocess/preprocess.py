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


def preprocess(
    only_query=False,
    only_users=False,
    save=True,
    return_preprocessed=False,
    workers=mp.cpu_count() - 1,
    tokenizer="nltk",
):
    pandarallel.initialize(nb_workers=workers, progress_bar=True)
    lengths = [0]
    load_filenames = (
        [os.path.join("data", "query", "query.json")] if not only_users else []
    ) + (
        [os.path.join("data", "users", user + ".json") for user in USERS_LIST]
        if not only_query
        else []
    )
    save_filenames = (
        [os.path.join("data", "query", "query.pkl")] if not only_users else []
    ) + (
        [os.path.join("data", "users", user + ".pkl") for user in USERS_LIST]
        if not only_query
        else []
    )
    tweets = pandas.DataFrame()
    if only_query or not (only_query or only_users):
        print("* LOADING QUERY TWEETS")
        tweets = pandas.read_json(
            load_filenames[0],
            orient="columns",
            convert_axes=False,
            convert_dates=False,
        )[["text"]]
        lengths.append(len(tweets))
    init = 1 if only_query or not (only_query or only_users) else 0
    for i in range(init, len(load_filenames)):
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
        lambda x: tweet_preprocess.preprocess(
            x.text, return_list=False, tokenizer=tokenizer,
        ),
        axis=1,
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
    only_query=False,
    only_users=False,
    save=True,
    return_preprocessed=False,
    workers=mp.cpu_count() - 1,
    tokenizer="nltk",
):
    pandarallel.initialize(nb_workers=workers, progress_bar=True)
    load_filenames = (
        [os.path.join("data", "query", "query.json")] if not only_users else []
    ) + (
        [os.path.join("data", "users", user + ".json") for user in USERS_LIST]
        if not only_query
        else []
    )
    save_filenames = (
        [os.path.join("data", "query", "query.pkl")] if not only_users else []
    ) + (
        [os.path.join("data", "users", user + ".pkl") for user in USERS_LIST]
        if not only_query
        else []
    )
    if return_preprocessed:
        preprocessed = [0] * len(load_filenames)

    for i in range(len(load_filenames)):
        if i == 0 and (only_query or not (only_query or only_users)):
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
            lambda x: tweet_preprocess.preprocess(
                x.text, return_list=False, tokenizer=tokenizer
            ),
            axis=1,
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


args = argparse.ArgumentParser(
    description="Preprocess tweets and save them to pickle files for future computation. For every tweet it create a list of preprocessed tokens"
)
args.add_argument(
    "-q", "--only-query", help="Preprocess only the query tweets", action="store_true",
)
args.add_argument(
    "-u", "--only-users", help="Preprocess only the users tweets", action="store_true",
)
args.add_argument(
    "-m",
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
    type=int,
)
args.add_argument(
    "-t",
    "--tokenizer",
    help="Which type of tokenizer to use: twitter or nltk",
    default="nltk",
    type=str,
)
args = args.parse_args()

if __name__ == "__main__":
    tweet_preprocess = TweetPreprocess()
    save = args.save
    only_query = args.only_query
    only_users = args.only_users
    if only_query and only_users:
        raise Exception("Only one of -q or -u must be used")
    if args.mem_oriented:
        preprocess_memory_oriented(
            only_query=only_query,
            only_users=only_users,
            save=save,
            return_preprocessed=False,
            workers=args.workers,
            tokenizer=args.tokenizer,
        )
    else:
        preprocess(
            only_query=only_query,
            only_users=only_users,
            save=save,
            return_preprocessed=False,
            workers=args.workers,
            tokenizer=args.tokenizer,
        )
