import tweepy
import json
import jsonpickle

consumer_key = "EQa4iFjD2wXsvYnysJwwn3m3R"
consumer_secret = "7uxYmpqUqNKr4Y1DCTSB0K3vEEWZ0lFNtmiQfovD954G81SUjL"
access_token = "1217000526887489536-YY8izIFzPq7WQwBo8tD3LTsP9ZbFTR"
access_token_secret = "nPQKtAIgjIZKOc01FIqKC3fOSr40SO3pkGOZDyRD9PHI8"

# Creating the authentication object
auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret

# Creating the API object while passing in auth information
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) 


def process_tweet(tweet, id):
	'''
		Create a tweet object with only important attribute
		list:
			id
			created_at
			text
			user
			location
			followers_count
			number_like
			number_retweet
			profile_image_url_https
			created_at
	'''
	tweets = []
	temp_tweet = {}

	temp_tweet['id'] = id
	temp_tweet['created_at'] = tweet.created_at.isoformat()
	temp_tweet['text'] = tweet.full_text
	temp_tweet['name_user'] = tweet.user.name
	temp_tweet['followers_count'] = int(tweet.user.followers_count)
	temp_tweet['like'] = int(tweet.favorite_count)
	temp_tweet['retweet'] = int(tweet.retweet_count)
	temp_tweet['profile_image_url'] = tweet.user.profile_image_url_https
	temp_tweet['tweet_url'] = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"

	return(temp_tweet)

def read_tweet_pre_downladed(filepath):
	
	# read and return json with tweet yet downloaded
	with open(filepath) as json_file:
		data = json.load(json_file)
	
	return data

maxTweets = 10000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
fName = './tweet.json' # We'll store the tweets in a text file.
tweet_list = read_tweet_pre_downladed(fName)

print('Numero di tweet già salvati nel json: ', len(tweet_list))

if len(tweet_list)==0:
	id_tweet = 1
else:
	id_tweet = tweet_list[len(tweet_list) - 1]['id']

searchQuery = "sport OR news OR music OR cinema OR technology OR religion OR war"

sinceId = None
max_id = 0

tweetCount = 0
print('Downloading max {0} tweets'.format(maxTweets))

# 45000 tweet every 15 minutes
with open(fName, 'w') as f:
	while tweetCount < maxTweets:
		try:
			if (max_id <= 0):
				if (not sinceId):
					new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended', lang='en', result_type='mixed', since='2020-01-14', include_entities=False)
				else:
					new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended', lang='en', result_type='mixed', since='2020-01-14', include_entities=False, since_id=sinceId)
			else:
				if (not sinceId):
					new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended', lang='en', result_type='mixed', since='2020-01-14', include_entities=False, max_id=str(max_id - 1))
				else:
					new_tweets = api.search(q=searchQuery, count=tweetsPerQry, tweet_mode='extended', lang='en', result_type='mixed', since='2020-01-14', include_entities=False, max_id=str(max_id - 1), since_id=sinceId)
			if not new_tweets:
				print("No more tweets found")
				break
			for tweet in new_tweets:
				tweet_list.append(process_tweet(tweet,id_tweet))
				id_tweet = id_tweet + 1
				#json.dump(tweet_list, f, indent=3)

			tweetCount = tweetCount + len(new_tweets)
			print('Downloaded {0} tweets'.format(tweetCount))
			max_id = new_tweets[-1].id

		except tweepy.TweepError as e:
			# Just exit if any error
			print("some error : " + str(e))
			break

print('Found: ', len(tweet_list), ' tweets')
print('Numero di tweet dopo averne scaricati altri: ', len(tweet_list))

with open(fName, 'w') as outfile:
	json.dump(tweet_list, outfile, indent=3)

# 2020 - 01 - 06
# 2019 - 12 - 29
# 2019 - 12 - 22
# 2019 - 12 - 15