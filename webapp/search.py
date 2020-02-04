import os
import json
import itertools
import numpy as np
from elasticsearch import Elasticsearch
from gensim.models.word2vec import Word2Vec
from gensim.models.phrases import Phraser
from preprocess.tweet_preprocess import TweetPreprocess
from config import USER_COUNTRY

bigram = Phraser.load(os.path.join("data", "models", "bigram.pkl"))
trigram = Phraser.load(os.path.join("data", "models", "trigram.pkl"))
query_embeddings = Word2Vec.load(os.path.join("data", "models", "query.model"))
user_embeddings = {}


def query_search(query, count, user, topic, method, bigrams, trigrams, location_search):
    client = Elasticsearch()

    expans = False
    # termini che possono comparire
    # mettiamo quelli del profilo utente
    # nel caso ci siano aumenta lo score del documento
    should = []

    # i termini che devono comparire
    # mettiamo il topic nel caso sia scelto dall'utente
    # per ricercare solo sui tweet di quel topic
    must = []
    str_profile = []
    must.append({"query_string": {"query": query, "default_field": "text"}})

    if user != "None":
        if method.startswith("bow"):
            ipath = os.path.join(
                "data",
                "users",
                "bow_tf.json" if method == "bow_tf" else "bow_tfidf.json",
            )
            with open(ipath) as jsonfile:
                bow = json.load(jsonfile)

            str_profile = " ".join(bow["@" + user])
            should.append({"match": {"text": str_profile}})
            expans = True
        elif method == "embeddings_mean" or method == "embeddings":
            user_embedding = None
            try:
                user_embedding = user_embeddings[user]
            except KeyError:
                user_embeddings[user] = Word2Vec.load(
                    os.path.join("data", "models", "@" + user + ".model")
                )
                user_embedding = user_embeddings[user]

            preprocessed_query = TweetPreprocess.preprocess(query)
            if bigrams:
                preprocessed_query = bigram[preprocessed_query]
            if trigrams:
                preprocessed_query = trigram[preprocessed_query]

            vectors = []
            shoulds = []
            for token in preprocessed_query:
                try:
                    vectors.append(query_embeddings.wv.get_vector(token))
                except KeyError:
                    print("Token " + token + " not found in query embeddings")
            if method == "embeddings_mean" and vectors != []:
                mean_vector = np.mean(vectors, axis=0)
                shoulds = [
                    word
                    for word, sim in user_embedding.wv.most_similar(
                        [mean_vector], topn=10
                    )
                ]
            elif method == "embeddings" and vectors != []:
                for vector in vectors:
                    shoulds.extend(
                        [
                            (word, sim)
                            for word, sim in user_embedding.wv.most_similar(
                                [vector], topn=10
                            )
                        ]
                    )
                shoulds = sorted(shoulds, key=lambda x: x[1], reverse=True)
                shoulds = [word for word, sim in shoulds]
                shoulds = list(dict.fromkeys(shoulds).keys())[:10]
                shoulds = [word.split("_") for word in shoulds]
                shoulds = list(itertools.chain(*shoulds))
                # Keep first 10 elements keeping order
            should.append({"match": {"text": " ".join(shoulds)}})
            expans = True

    # possibile filtraggio a priori per topic
    if topic != "None":
        must.append({"term": {"topic": topic}})

    # amento rilevnza documenti che hanno country_code uguale a quello dell'utente
    if user != "None":
        should.append({"term": {"country": USER_COUNTRY[user]}})

    # aumento rilevanza dei documenti che sono molto popolari (retweet e like)
    #should.append({"rank_feature": {"field": "popularity.retweet", "boost": 5}})
    #should.append({"rank_feature": {"field": "popularity.like", "boost": 5}})

    #should.append(
    #    {"distance_feature": {"field": "created_at", "pivot": "5d", "origin": "now", "boost": 15}}
    #)

    print("SHOULD", should)

    q = {"must": must, "should": should}
    body = {"size": count, 
            "query": {
                "function_score": {
                    "query": {
                        "bool": q
                    },
                    "functions": [
                        {
                          "exp": {
                            "created_at": {
                              "origin": "now", 
                              "scale": "10d",
                              "offset": "5d",
                              "decay" : 0.6
                            }
                          }
                        },
                        {
                        "field_value_factor": {
                            "field": "like",
                            "factor": 1,
                            "modifier": "sqrt",
                            "missing": 1
                        }
                        },
                        {
                        "field_value_factor": {
                            "field": "retweet",
                            "factor": 1,
                            "modifier": "sqrt",
                            "missing": 1
                        }
                        }
                    ],
                    "score_mode": "multiply"
                }
            }
        }
    res = client.search(index="index_twitter", body=body)
    res = res["hits"]["hits"]
    # print('Ho trovato: ', len(res), ' tweet')

    if expans:
        return res, should[0]["match"]["text"]
    else:
        return res, " "
