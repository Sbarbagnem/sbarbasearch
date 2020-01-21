from elasticsearch import Elasticsearch


def query_search(query, count_result):
    client = Elasticsearch()

    # per ridurre i dati ritornati
    # filter_path=['hits.hits._id', 'hits.hits._type']

    # control if is a boolean query like 'term1 AND term2'
    if query[0] == "'" and query[-1] == "'":
        # print(query)
        query = query[1:-1]
        body = {
            "sort": [
                "_score",
                {"followers_count": {
                    "order": "desc"}
                },
                {"retweet": {
                    "order": "desc"}
                }
            ],
            "query": {
                "query_string": {
                    "query": query,
                    "default_field": "text"
                }
            }
        }

    else:
        body = {
            "sort": [
                "_score",
                {"followers_count": {"order": "desc"}},
                {"retweet": {"order": "desc"}}
            ],
            "query": {
                "match": {
                    "text": {
                        "query": query
                    }
                }
            }
        }

    res = client.search(index="index_twitter", body=body, size=count_result)

    res = res['hits']['hits']

    # print('Ho trovato: ', len(res), ' tweet')

    return res
