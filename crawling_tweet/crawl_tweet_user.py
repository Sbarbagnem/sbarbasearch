import os
import json
import tweepy
from secret import CONSUMER_KEY, CONSUMER_SECRET


def crawl_tweet_for_user_no_limits(user, count=200, update=True):

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(
        screen_name=user, count=count, tweet_mode="extended", include_entities=False
    )

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(
            screen_name=user,
            count=count,
            max_id=oldest,
            tweet_mode="extended",
            include_entities=False,
        )

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    # print(tweets_list)
    tweets = {}

    if update:
        user_path = os.path.join("..", "user_profile", "data", user + ".json")
        tweets = json.load(open(user_path, "rb"))

    for tweet in alltweets:
        # tengo solo testo del tweet
        if hasattr(tweet, 'retweeted_status'):
            tweets[tweet.id_str] = tweet.retweeted_status.full_text
        else:
            tweets[tweet.id_str] = tweet.full_text

    return tweets

def save_tweer_for_user(user, tweets):

    with open("../user_profile/data/" + user + ".json", "w") as outfile:
        json.dump(tweets, outfile, indent=3)


if __name__ == "__main__":

    auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    PATH_JSON_TWEET_FOR_USER = "./tweet_for_user.json"

    # two real user for every topic
    list_user = [
        "@MarcusRashford",
        "@AaronDonald97",
        "@GreenDay",
        "@MartinGarrix",
        "@EmmaWatson",
        "@VancityReynolds",
        "@elonmusk",
        "@IBM",
        "@realDonaldTrump",
        "@BorisJohnson",
        "@Yunus_Centre",
        "@JosephEStiglitz",
    ]

    # per ogni utente nella list_user scarico gli utlimi tweet publicati
    for user in list_user:
        print("Scarico tweet di ", user)
        tweets = crawl_tweet_for_user_no_limits(user, count=10000, update=False)
        # print(tweets)
        # salvo tweet in json user.json
        save_tweer_for_user(user, tweets)
