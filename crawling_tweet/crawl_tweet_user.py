import os
import json
import tweepy
from config import USERS_LIST, CONSUMER_KEY, CONSUMER_SECRET


def crawl_tweet_for_user_no_limits(user, count=200, update=False):

    # initialize a list to hold all the tweepy Tweets
    alltweets = []
    # print(tweets_list)
    tweets = {}

    if update:
        user_path = os.path.join("data", "users", user + ".json")
        tweets = json.load(open(user_path, "rb"))
        since_id = int(list(tweets.keys())[0]) - 1
        new_tweets = api.user_timeline(
            screen_name=user,
            count=count,
            since_id=since_id,
            tweet_mode="extended",
            include_entities=False,
        )
        newest = new_tweets[-1].id - 1
    else:
        new_tweets = api.user_timeline(
            screen_name=user, count=count, tweet_mode="extended", include_entities=False
        )
        oldest = new_tweets[-1].id - 1

    # save most recent tweets
    alltweets.extend(new_tweets)

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest if not update else newest))

        if update:
            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(
                screen_name=user,
                count=count,
                since_id=newest,
                tweet_mode="extended",
                include_entities=False,
            )
            if len(new_tweets) > 0:
                newest = new_tweets[-1].id - 1
        else:
            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(
                screen_name=user,
                count=count,
                max_id=oldest,
                tweet_mode="extended",
                include_entities=False,
            )
            if len(new_tweets) > 0:
                oldest = new_tweets[-1].id - 1

        # save most recent tweets
        alltweets.extend(new_tweets)

        print("...%s tweets downloaded so far" % (len(alltweets)))

    for tweet in alltweets:
        # tengo solo testo del tweet
        if hasattr(tweet, "retweeted_status"):
            tweets[tweet.id_str] = tweet.retweeted_status.full_text
        else:
            tweets[tweet.id_str] = tweet.full_text

    return tweets


def save_tweer_for_user(user, tweets):

    with open(os.path.join("data", "users", user + ".json"), "w") as outfile:
        json.dump(tweets, outfile, indent=3)


if __name__ == "__main__":

    auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # per ogni utente nella USERS_LIST scarico gli utlimi tweet publicati
    for user in USERS_LIST:
        print("Scarico tweet di ", user)
        tweets = crawl_tweet_for_user_no_limits(user, count=10000, update=True)
        # print(tweets)
        # salvo tweet in json user.json
        save_tweer_for_user(user, tweets)
