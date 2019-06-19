import tweepy
import numpy as np
import time
import string
from twython import Twython
import json
from sklearn import preprocessing
from data_collection import get_latest_tweets
import gensim
from nltk.corpus import stopwords


def tokenize_tweet(tweet):
    tokens = [str(word) for word in str(tweet).lower().split()]
    return(tokens)


def remove_punctuation(tokens):
    clean_words = [word.translate(str.maketrans('', '', string.punctuation)) for word in tokens]
    return(clean_words)


def clean_text(model, clean_words):
    stoplist = set(stopwords.words('english'))
    tweet_nostopwords = [word for word in clean_words if word not in stoplist]
    filtered_word_list = [word for word in tweet_nostopwords if word in model.vocab]
    return(filtered_word_list)


def tweet_preprocess(row_tweet, model):
    return clean_text(model, remove_punctuation(tokenize_tweet(row_tweet)))


def vectorize_tweet(normalized_tweet,model):
    vec=np.zeros((300))
    for word in normalized_tweet:
        vec += model[word] 
    return preprocessing.normalize(vec.reshape(1,-1))


def vectorize_latest_tweets(tweets, model):
    print('vectorizing tweets...')
    tic = time.time()
    tweets.loc[:,'normalized'] = tweets.tweet.apply(lambda tweet: tweet_preprocess(tweet, model))
    tweets.loc[:,'vector'] = tweets.normalized.apply(lambda tweet: vectorize_tweet(tweet, model))
    toc=time.time()
    print('tweets vectorizd in '+ str((toc-tic)/60)+' minutes')
    return tweets


def vectorize_user_input(user_input, model):
    
    print('vectorizing user_input...')
    normalized = tweet_preprocess(user_input, model)
    word_vec = vectorize_tweet(normalized, model)
    vectorized_input = {'raw_input': user_input, 'normalized': normalized, 'vector': word_vec}      
    print('user_input is vectorized!')
    return vectorized_input


if __name__ == '__main__':
    data_dir='./'
    topic = 'Canada' # it can be a list of topics,  comman means 'or'
    time_limit = 20 # time_limist seconds of  streaming data
    with open(data_dir + "twitter_credentials.json", "r") as file:  
         credentials = json.load(file)
    # Instantiate an object
    python_tweets = Twython( credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
    auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
    auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
    tweets, no_data = get_latest_tweets(data_dir, auth, time_limit, topic)
    if no_data:
        print('There is no data with topic: '+ topic +' in  '+ str(time_limit) +' seconds')
    else:
        print('uploading the model...')
        model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary = True)
        vectorized_tweets = vectorize_latest_tweets(tweets, model)
        vectorized_tweets


        

