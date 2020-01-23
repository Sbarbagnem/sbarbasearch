import pandas as pd
import json
#from sklearn.feature_extraction.text import TfidfVectorizer
from twitter_preprocessor import TwitterPreprocessor
import os
import re
from collections import Counter

def processing_tweet(sentence):
    p = TwitterPreprocessor(sentence)
    p.fully_preprocess()
    return p.text

def word_count(str):
    # frequenza parole in tweet
    
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts


if __name__ == '__main__':

    PATH_TWEET_FOR_USER = './data/'

    directory = os.fsencode(PATH_TWEET_FOR_USER)

    bow = []


    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json"): 
            user = re.split('@|.json', filename)[1]

            with open(PATH_TWEET_FOR_USER + filename) as jsonfile:
                tweets = json.load(jsonfile)
                tweets = ' '.join(tweets)
                tweet_processed = processing_tweet(tweets)
                words = re.findall(r'\w+', tweet_processed)
                ten_common_frequency = Counter(words).most_common(10)
                ten_common = [word[0] for word in ten_common_frequency]
                temp = {str(user): ten_common}
                #print(temp)
                bow.append(temp)

    with open('./data/bow.json', 'w') as jsonfile:
        json.dump(bow, jsonfile, indent=3)

