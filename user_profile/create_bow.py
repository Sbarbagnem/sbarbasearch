import os
import time
import json
import pickle
import numpy as np
from config import USERS_LIST
from gensim.models.phrases import Phraser
from sklearn.feature_extraction.text import TfidfVectorizer

if __name__ == "__main__":

    bow = {}
    compute_n_grams = True

    if compute_n_grams:
        bigram = Phraser.load(os.path.join("data", "models", "bigram.pkl"))
        trigram = Phraser.load(os.path.join("data", "models", "trigram.pkl"))

    for user in USERS_LIST:
        print("* LOADING " + user + " SENTENCES")
        user_sentences = pickle.load(
            open(os.path.join("data", "users", user + ".pkl"), "rb")
        )
        if compute_n_grams:
            print("* COMPUTING BIGRAMS/TRIGRAMS")
            user_sentences = trigram[bigram[user_sentences]]
        user_sentences = map(lambda sentence: " ".join(sentence), user_sentences)
        tfidf = TfidfVectorizer(
            lowercase=False,
            analyzer="word",
            tokenizer=lambda x: x.split(),
            token_pattern=None,
        )
        print("* TF-IDF")
        X = tfidf.fit_transform(user_sentences)
        features = np.array(tfidf.get_feature_names())
        tfidf_sorting = np.argsort(X.toarray()).flatten()[::-1]
        top_n = features[tfidf_sorting][:10]
        bow[user] = top_n.tolist()

    with open(os.path.join("data", "users", "bow.json"), "w") as f:
        json.dump(bow, f)
