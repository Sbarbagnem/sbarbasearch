import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from twitter_preprocessor import TwitterPreprocessor

def processing_tweet(sentence):
    p = TwitterPreprocessor(sentence)
    p.fully_preprocess()
    return p.text

def tf_idf_for_user_topic(data):
    for user in USERS:
        for topic in TOPICS:
            temp_data = data.loc[(data['user'] == user) & (data['topic'] == topic)]
            print(temp_data.empty)
            term, value = tf_idf(temp_data)
            print(term)
            print(value)

def tf_idf(data):
    v = TfidfVectorizer()
    x = v.fit_transform(data['tweet_processed'])

    df = pd.DataFrame(x.toarray(), columns=v.get_feature_names())
    #df.drop('text', axis=1, inplace=True)
    #res = pd.concat([df, df1], axis=1)

    # mean for every word
    df.loc['mean'] = df.mean()
    df = df.sort_values(by='mean', axis=1)

    # return top 15 word with highest tf_idf
    list_term = list(df.columns[0:15])
    list_value = df[-1:].loc[:, list_term].values.tolist()[0]

    return list_term, list_value

if __name__ == '__main__':

    PATH_DATASET = './dataframe_tweet_for_user.csv'

 #   TOPICS = ['sport', 'music', 'cinema', 'technology', 'religion', 'war', 'economy']
 #   USERS = ['user_1', 'user_2', 'user_3', 'user_4', 'user_5', 'user_6', 'user_7', 'user_8', 'user_9', 'user_10']

    TOPICS = ['sport']
    USERS = ['user_1']
    dataset = pd.read_csv(PATH_DATASET) 

    # processing tweet text
    dataset['tweet_processed'] = dataset['tweet'].apply(processing_tweet)

    dataset.to_csv('tweet_for_user_processed.csv',index=True)

    # tf-idf for every user and every topic 
    dataset = tf_idf_for_user_topic(dataset)


