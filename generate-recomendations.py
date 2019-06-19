from tweepy import Stream
import pandas as pd
import numpy as np
import tweepy
from twython import Twython
import json
import gensim
import os
from data_collection import get_latest_tweets
from data_preprocessing import vectorize_latest_tweets, vectorize_user_input


def find_most_similar_tweets(vectorized_input, vectorized_tweets, topn, model):
    vec_tweets = np.vstack(vectorized_tweets.vector.apply(lambda x: x.tolist()))
    cos=model.cosine_similarities(vectorized_input['vector'].reshape(-1,), vec_tweets)
    vectorized_tweets.loc[:,'similarity_score'] = cos 
    vectorized_tweets = vectorized_tweets.sort_values(by='similarity_score', ascending=False)
    return vectorized_tweets[0:topn]


def process_user_input(user_input, time_limit, topic, topn):

    track_list = [k for k in topic.split(',')]
    file_name = "stream"
    if os.path.exists(data_dir+file_name + '.json'):
        os.remove(data_dir + file_name + '.json')
    #-----------------------------------------------
    # Load credentials from json file
    tweets, no_data = get_latest_tweets(data_dir, auth, time_limit, track_list)
    if no_data:
        return 'There is no data with topic: '+ topic +' in  '+ str(time_limit) +' seconds'
    else:
        print('uploading the model...')
        model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary = True)
        vectorized_tweets = vectorize_latest_tweets(tweets, model)
        vectorized_user_input = vectorize_user_input(user_input, model)
        # find the top topn= 10  similar tweets
        recommendations = find_most_similar_tweets(vectorized_user_input, vectorized_tweets, topn, model)
        print('top '+ str(topn) + ' similar tweets are obtained!')
    return recommendations[0:topn]

if __name__ == '__main__':
    topn = 10
    data_dir='./'
    topic = 'Canada' #it can be a list of topics,  comman means 'or'
    time_limit = 20 # time_limist seconds of  streaming data
    user_input = 'tariff'
    with open(data_dir + "twitter_credentials.json", "r") as file:
         credentials = json.load(file)
    # Instantiate an object
    python_tweets = Twython( credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
    auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
    auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
    recommendations = process_user_input(user_input, time_limit, topic, topn)
