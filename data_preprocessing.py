import numpy as np
import time
import string
from sklearn import preprocessing
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


def vectorize_tweet(normalized_tweet, model):
    vec=np.zeros((300))
    for word in normalized_tweet:
        vec += model[word] 
    return preprocessing.normalize(vec.reshape(1, -1))


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