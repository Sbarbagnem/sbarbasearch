import os
import logging
import argparse
import multiprocessing as mp
from twec.twec import TWEC
from config import USERS_LIST
from gensim.models.word2vec import Word2Vec

logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)

args = argparse.ArgumentParser(
    description="Learn a TWEC model with compass and temporal slices. It takes as input a txt with all the vocabs, compass.txt and a .txt file for every slices, in this case one for the query and one for every user"
)
args.add_argument(
    "--size",
    help="Size of the embeddings. A multiple of 4 is preferred",
    default=56,
    type=int,
)
args.add_argument(
    "--sg",
    help="Whether to use the CBOW (0) or the SKIP-GRAM (1) model of Word2Vec. Default CBOW",
    default=0,
    type=int,
)
args.add_argument(
    "--iter",
    help="Number of epochs of training for the compass and for the slices: --iter 20 30 it will train the compass model for 20 epochs and the slices for 30 epochs",
    nargs="+",
    type=int,
    default=[20, 20],
)
args.add_argument(
    "-w",
    "--workers",
    help="How many cores to use during the preprocessing. Default system-cores - 1",
    default=mp.cpu_count() - 1,
    type=int,
)
args = args.parse_args()

"""
:param size: Number of dimensions. Default is 100.
:param sg: Neural architecture of Word2vec. Default is CBOW (). If 1, Skip-gram is employed.
:param siter: Number of static iterations (epochs). Default is 5.
:param diter: Number of dynamic iterations (epochs). Default is 5.
:param ns: Number of negative sampling examples. Default is 10, min is 1.
:param window: Size of the context window (left and right). Default is 5 (5 left + 5 right).
:param alpha: Initial learning rate. Default is 0.025.
:param min_count: Min frequency for words over the entire corpus. Default is 5.
:param workers: Number of worker threads. Default is 2.
:param test: Folder name of the diachronic corpus files for testing.
:param opath: Name of the desired output folder. Default is model.
:param init_mode: If \"hidden\" (default), initialize temporal models with hidden embeddings of the context;'
                    'if \"both\", initilize also the word embeddings;'
                    'if \"copy\", temporal models are initiliazed as a copy of the context model
                    (same vocabulary)
"""

if __name__ == "__main__":

    aligner = TWEC(
        size=args.size,
        sg=args.sg,
        siter=args.iter[0],
        diter=args.iter[1],
        workers=args.workers,
        opath=os.path.join("data", "models"),
    )
    aligner.train_compass(
        os.path.join("data", "twec", "compass.txt"), overwrite=True
    )  # keep an eye on the overwrite behaviour
    aligner.train_slice(os.path.join("data", "twec", "query.txt"), save=True)
    for user in USERS_LIST:
        aligner.train_slice(os.path.join("data", "twec", user + ".txt"), save=True)
