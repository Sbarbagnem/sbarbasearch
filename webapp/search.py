import os
import json
import itertools
import numpy as np
from elasticsearch import Elasticsearch
from gensim.models.word2vec import Word2Vec
from gensim.models.phrases import Phraser
from preprocess.tweet_preprocess import TweetPreprocess
from config import USER_COUNTRY

bigram = Phraser.load(os.path.join("compass_embeddings", "model", "bigram.pkl"))
trigram = Phraser.load(os.path.join("compass_embeddings", "model", "trigram.pkl"))
query_embeddings = Word2Vec.load(
    os.path.join("compass_embeddings", "model", "query_tweets.model")
)
user_embeddings = {}


def query_search(query, count_result, user, topic, method, location_search):
    client = Elasticsearch()

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
        if method == "bow":
            with open(
                os.path.join("user_profile", "data", "bow.json")
            ) as jsonfile:
                data = json.load(jsonfile)

            for bow in data:
                if list(bow.keys())[0] == user:
                    # should.extend([{"term": {"text": str(word)}} for word in bow[user]])
                    str_profile = " ".join(str(word) for word in bow[user])
                    should.append({"match": {"text": str_profile}})
        elif method == "embeddings_mean" or method == "embeddings":
            user_embedding = None
            try:
                user_embedding = user_embeddings[user]
            except KeyError:
                user_embeddings[user] = Word2Vec.load(
                    os.path.join(
                        "compass_embeddings", "model", "@" + user + "_tweets.model"
                    )
                )
                user_embedding = user_embeddings[user]

            preprocessed_query = trigram[bigram[TweetPreprocess.preprocess(query)]]
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
                should.append({"match": {"text": " ".join(shoulds)}})
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
                should.append(
                    {
                        "match": {
                            "text": " ".join(shoulds)
                        }
                    }
                )

    # possibile filtraggio a priori per topic
    if topic != "None":
        must.append({"term": {"topic": topic}})
        
    # amento rilevnza documenti che hanno country_code uguale a quello dell'utente
    should.append({"term": {"country": USER_COUNTRY[user]}})

    # aumento rilevanza dei documenti che sono molto popolari (retweet e like)
    should.append({"rank_feature": {"field": "popularity.retweet","boost": 10}})
    should.append({"rank_feature": {"field": "popularity.like","boost": 10}})

    # possibile aumento di rilevanza sulla base della distanza coordinate_tweet e coordinate_ricerca
    # simuliamo una sorta di ricerca personalizzata sulla base della localizzazione
    if location_search != 'None':
        should.append({ 
                        "distance_feature": {
                            "field": "location",
                            "pivot": "200km",
                            "origin": location_search,
                            "boost": 5
                        }
                    }
        )
    
    should.append({
        "distance_feature": {
          "field": "created_at",
          "pivot": "7d",
          "origin": "now"
        }
      })

    print("SHOULD", should)

    q = {"must": must, "should": should}
    body = {"size": count_result, "query": {"function_score": {"query": {"bool": q}}}}
    res = client.search(index="index_twitter", body=body)
    res = res["hits"]["hits"]
    # print('Ho trovato: ', len(res), ' tweet')

    return res
