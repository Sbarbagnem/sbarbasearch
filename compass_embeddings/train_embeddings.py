import os
from twec.twec import TWEC
from gensim.models.word2vec import Word2Vec
from config import USERS_LIST

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
aligner = TWEC(size=50, sg=0, siter=30, diter=30, workers=7)
aligner.train_compass(
    os.path.join(".", "data", "compass.txt"), overwrite=True
)  # keep an eye on the overwrite behaviour
aligner.train_slice(os.path.join(".", "data", "query_tweets.txt"), save=True)
for user in USERS_LIST:
    aligner.train_slice(os.path.join(".", "data", user + "_tweets.txt"), save=True)