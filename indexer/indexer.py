from elasticsearch import Elasticsearch
from elasticsearch import helpers
import json

es = Elasticsearch(hosts=["localhost"])

def index_exist(name_index):
    return es.indices.exists(index=name_index)

def delete_index(name_index):
    es.indices.delete(index=name_index)

def create_index():

    mapping = {
        "settings" : {
            "index" : {
            "number_of_shards" : 1,
            "number_of_replicas" : 0
            },
            "analysis": {
            "analyzer": {
                "custom_analyzer": {
                "type": "custom",
                "tokenizer": "whitespace",
                "filter": [
                    "lowercase"
                ]
                }
            }
            }
        },
        "mappings": {
            "properties": {
                "created_at": {
                    "type": "date",
                    "index": False,
                    "store" : True
                },
                "text": {
                    "type": "text",
                    "store" : True,
                    "analyzer" : "custom_analyzer"
                },
                "user": {
                    "type": "text",
                    "store" : True,
                    "analyzer" : "custom_analyzer"
                },
                "followers_count": {
                    "type": "integer",
                    "index": False,
                    "store" : True
                },
                "like": {
                    "type": "integer",
                    "index": False,
                    "store" : True
                },
                "retweet": {
                    "type": "integer",
                    "index": False,
                    "store" : True
                },
                "profile_image": {
                    "type": "keyword",
                    "index": False,
                    "store" : True
                },
                "tweet_url": {
                    "type": "keyword",
                    "index": False,
                    "store" : True
                }
            }
        }
    }

    # make an API call to the Elasticsearch cluster
    # and have it return a response:
    response = es.indices.create(
        index="index_twitter",
        body=mapping,
        ignore=400 # ignore 400 already exists code
    )

    if 'acknowledged' in response:
        if response['acknowledged'] == True:
            print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])

    # catch API error response
    elif 'error' in response:
        print ("ERROR:", response['error']['root_cause'])
        print ("TYPE:", response['error']['type'])

    # print out the response:
    print ('\nresponse:', response)


  
def write_tweet_on_index(filepath):
    # read tweet.json and add every tweet to index
    with open(filepath) as json_file:
        
        data = json.load(json_file)
        
        jsonvalue = []

        chunk_size = len(data)

        for tweet in data:

            body = {
                '_op_type': 'create',
                '_index': 'index_twitter',
                #'_type': 'tweet',
                '_id': tweet['id'],
                'created_at': tweet['created_at'],
                'text': tweet['text'],
                'user': tweet['name_user'],
                'followers_count': tweet['followers_count'],
                'like': tweet['like'],
                'retweet': tweet['retweet'],
                'profile_image': tweet['profile_image_url'],
                'tweet_url': tweet['tweet_url']
            }

            jsonvalue.append(body)

        res = helpers.bulk(es, jsonvalue, chunk_size=chunk_size, request_timeout=600, stats_only=True)

if __name__ == '__main__':

    NAME_INDEX = 'index_twitter'

    if index_exist(NAME_INDEX):
        delete_index(NAME_INDEX)

    create_index()
    write_tweet_on_index('../crawling_tweet/tweet.json')
    print('index creato e popolato')
    exit()
