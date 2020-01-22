from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import json
from setting_analyzer import MAPPING

def index_exist():
    return client.indices.exists(index=NAME_INDEX)

def delete_index():
    client.indices.delete(index=NAME_INDEX)

def read_tweet_pre_downladed(filepath):
	
	# read and return json with tweet yet downloaded
	with open(filepath) as json_file:
		data = json.load(json_file)
	
	return data

def create_index():

    # make an API call to the Elasticsearch cluster
    # and have it return a response:
    response = client.indices.create(
        index="index_twitter",
        body=MAPPING,
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


  
def write_tweet_on_index():
    # read tweet.json and add every tweet to index

    tweets = read_tweet_pre_downladed(PATH_TO_JSON_TWEET)

    tweet_list = []
    count = 0

    for tweet in tweets:

        tweet_list.append(tweet)
        count += 1

        if count % BATCH == 0:
            index_batch(tweet_list)
            tweet_list = []
            print("Indexed {} tweets.".format(count))

    if tweet_list:
        index_batch(tweet_list)
        print("Indexed {} tweets.".format(count))

    client.indices.refresh(index=NAME_INDEX)

def index_batch(tweets):

    requests = []

    for tweet in tweets:
        request = {
            '_op_type': 'index',
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
            'tweet_url': tweet['tweet_url'],
            'topic': tweet['topic']
        }
        requests.append(request)

    bulk(client, requests, chunk_size=len(requests), request_timeout=600, stats_only=True)

if __name__ == '__main__':

    client = Elasticsearch(hosts=["localhost"])

    NAME_INDEX = 'index_twitter'
    # batch to upload n tweet for bulk
    BATCH = 10000
    PATH_TO_JSON_TWEET = '../crawling_tweet/tweet.json'

    if index_exist():
        print('Esiste già l\'index')
        delete_index()
        print('Index eliminato')

    create_index()
    print('Index creato')
    write_tweet_on_index()
    print('index creato e popolato')
