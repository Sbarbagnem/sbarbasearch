from elasticsearch import Elasticsearch
import json

def query_search(query, count_result, user, topic):
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

    must.append({"query_string":{ "query":query, "default_field": "text"}})

    if user != 'None':

        with open('../user_profile/data/bow.json') as jsonfile:
            data = json.load(jsonfile)
        
        for bow in data:
            if list(bow.keys())[0] == user:
                #should.extend([{"term": {"text": str(word)}} for word in bow[user]])
                str_profile = ' '.join(str(word) for word in bow[user])
                should.append({"match": {"text": str_profile}})
                

    if topic != 'None':
        must.append({"term": {"topic": topic}})
        #topic_filter = {"filter":{"term": {"topic": topic}}}

    q = {"must": must,"should": should}

    body = {
        "size":count_result,
            "query": {
                "function_score": {
                    "query": {
                        "bool": q
                    }
                }
            }
        }


    res = client.search(index="index_twitter", body=body)

    res = res['hits']['hits']

    # print('Ho trovato: ', len(res), ' tweet')

    return res
