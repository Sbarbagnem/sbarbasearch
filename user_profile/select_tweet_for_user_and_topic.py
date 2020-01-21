import json
from random import randrange
import pandas as pd

def load_tweet_for_user():

    index = 0

	# per ogni utente prendo circa 100 tweet random per ogni topic
    for user in USERS:
        for topic in TOPICS:
            last_index = load_tweet_for_topic(user,topic,100,index)
            index = last_index

def load_tweet_for_topic(user,topic,number_tweets,index):
    
    with open(FILEPATH_TWEET) as json_file:
        data = json.load(json_file)

    tweet_topic = [tweet for tweet in data if tweet['topic'] == topic]

    list_id = [tweet['id'] for tweet in tweet_topic]
    min_id = min(list_id)
    max_id = max(list_id)

    # genero 100 random id tra il min e il max
    list_id=[]
    i = 0
   
    while i < 100:
        r = randrange(min_id,max_id)
        if r not in list_id: 
            list_id.append(r)
            i = i + 1

    tweet_100_topic = [tweet['text'] for tweet in tweet_topic if tweet['id'] in list_id]

    for tweet in tweet_100_topic:
        index = index + 1
        DATASET.loc[str(index)] = [user, topic, tweet]
    
    print('Ho selezionato ', number_tweets, ' per l\'utente ', user, ' per il topic ', topic)

    return index


if __name__ == '__main__':

    FILEPATH_TWEET = '../crawling_tweet/tweet_prova.json'
    FILEPATH_USER_PROFILE = './dataframe_tweet_for_user.csv'
    TOPICS = ['sport', 'music', 'cinema', 'technology', 'religion', 'war', 'economy']
    USERS = ['user_1', 'user_2', 'user_3', 'user_4', 'user_5', 'user_6', 'user_7', 'user_8', 'user_9', 'user_10']
    '''USERS_PROFILE = {   'user_1': {},
                        'user_2': {},
                        'user_3': {},
                        'user_4': {},
                        'user_5': {},
                        'user_6': {},
                        'user_7': {},
                        'user_8': {},
                        'user_9': {},
                        'user_10': {} }'''

    DATASET = pd.DataFrame(columns=['user', 'topic', 'tweet'])

    load_tweet_for_user()

    DATASET.to_csv(FILEPATH_USER_PROFILE,index=False)