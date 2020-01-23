import tweepy
import json
import jsonpickle
from secret import CONSUMER_KEY, CONSUMER_SECRET

def crawl_tweet_for_user(user):
    '''
        scarico ultimi 20 tweet di user
    '''

    tweets = []

    tweets_list = api.user_timeline(screen_name=user, count=20, tweet_mode='extended', include_entities=False)

    #print(tweets_list)

    for tweet in tweets_list:

        # tengo solo testo del tweet
        tweets.append(tweet.full_text)

    return tweets

def save_tweer_for_user(user, tweets):
	
    with open('../user_profile/data/' + user + '.json', 'w') as outfile:
        json.dump(tweets, outfile, indent=3)

if __name__ == '__main__':

    auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) 

    PATH_JSON_TWEET_FOR_USER = './tweet_for_user.json'

    # two real user for every topic
    list_user = ['@MarcusRashford','@AaronDonald97', '@GreenDay', '@MartinGarrix', '@EmmaWatson', '@vindiesel', '@elonmusk', '@IBM', '@realDonaldTrump', '@BorisJohnson', '@Yunus_Centre', '@JosephEStiglitz']

    # per ogni utente nella list_user scarico gli utlimi 20 tweet publicati
    for user in list_user:
        print('Scarico tweet di ', user)
        tweets = crawl_tweet_for_user(user)
        #print(tweets)
        # salvo tweet in json user.json
        save_tweer_for_user(user, tweets)