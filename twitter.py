from tweepy import Stream
import pandas as pd
import numpy as np
import tweepy
from tweepy.streaming import StreamListener
import time
import string
from twython import Twython
import json
from sklearn import preprocessing
import gensim
import os
from nltk.corpus import stopwords


def get_latest_tweets(data_dir, auth, time_limit, topic):

    print("streaming tweets...")
    tic = time.time()
    twitter_stream = Stream(auth, MyListener(data_dir, time_limit), tweet_mode='extended')
    twitter_stream.filter(track = topic) # list of querries to track
    t = time.time()
    print('stream data are saved in '+ str((t-tic)/60)+' minutes')
    print('reading stream file...')
    data = pd.read_json(data_dir+"stream.json", lines=True)
    ll = time.time()
    print('reading the stream file takes ' + str((ll-t)/60) +' minutes')
    tweets = pd.DataFrame(columns=['time', 'tweet'], index=data.index)
    print('getting full_text tweets...')
    no_data = False
    if data.empty:
        no_data = True
    else:
        data = data[data.lang == 'en']
        tweets=pd.DataFrame(columns = ['time','tweet'], index=data.index)
        tweets['tweet'] = data.apply(lambda x: get_full_text_tweet(x), axis = 1)
        tweets['time'] = data.created_at
        tweets = tweets.sort_values('time', ascending=False)
        tweets = tweets.drop_duplicates()
        tweets = tweets.dropna(subset = ['tweet'])
    toc = time.time()
    print(str(tweets.shape[0])+ ' full_text tweets obtained in ' + str((toc-tic)/60) + ' minutes', tweets)
    return tweets, no_data
# ---------------------------------------------
def get_full_text_tweet(tweet):
   if pd.isnull(tweet.retweeted_status):
         if pd.isnull(tweet.extended_tweet):
                full_text = tweet.text
         else:   
            if "full_text" in tweet.extended_tweet.keys():
                 full_text = tweet.extended_tweet["full_text"]

            else:
                 full_text = tweet.text 
   else:
        if 'extended_tweet' in tweet.retweeted_status.keys():
            if "full_text" in tweet.retweeted_status['extended_tweet'].keys():
                full_text = tweet.retweeted_status['extended_tweet']["full_text"]
        else:
             full_text = tweet.retweeted_status['text']    
   return full_text 
#--------------------------------------------
#MyListener() saves the data into a .json file with name stream
class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, data_dir, time_limit):
        self.start_time = time.time()
        self.limit = time_limit
        self.saveFile = open(data_dir + "stream.json", 'a')
        super(MyListener, self).__init__()

    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            self.saveFile.write(data)
            return True
        else:
            self.saveFile.close()
            return False
            

    def on_error(self, status):
        print(status)
        return True
# ----------------------------------------
def tokenize_tweet(tweet):
    tokens = [str(word) for word in str(tweet).lower().split()];
    return(tokens);

def remove_punctuation(tokens):
    clean_words = [word.translate(str.maketrans('', '', string.punctuation)) for word in tokens]
    return(clean_words)

def clean_text(model, clean_words):
    stoplist = set(stopwords.words('english'))
    tweet_nostopwords = [word for word in clean_words if word not in stoplist]
    filtered_word_list = [word for word in tweet_nostopwords if word in model.vocab]
    return(filtered_word_list)
# ----------------------------------------------------
def tweet_preprocess(row_tweet,model):
    return clean_text(model,remove_punctuation(tokenize_tweet(row_tweet)))
# ------------------------------------------------------


def vectorize_tweet(normalized_tweet,model):
    vec=np.zeros((300))
    for word in normalized_tweet:
        vec += model[word] 
    return preprocessing.normalize(vec.reshape(1,-1))
# -----------------------------------------------------


def vectorize_latest_tweets(tweets, model):
    
    print('vectorizing tweets...')
    tic = time.time()
    tweets.loc[:,'normalized'] = tweets.tweet.apply(lambda tweet: tweet_preprocess(tweet, model))
    tweets.loc[:,'vector'] = tweets.normalized.apply(lambda tweet: vectorize_tweet(tweet, model))
    toc=time.time()
    print('tweets vectorizd in '+ str((toc-tic)/60)+' minutes')
    return tweets

# ---------------------------------------------------

def vectorize_user_input(user_input, model):
    
    print('vectorizing user_input...')
    normalized = tweet_preprocess(user_input, model)
    word_vec = vectorize_tweet(normalized, model)
    vectorized_input = {'raw_input': user_input, 'normalized': normalized, 'vector': word_vec}      
    print('user_input is vectorized!')
    return vectorized_input
# ---------------------------------------------------

def find_most_similar_tweets(vectorized_input, vectorized_tweets, topn):
    vec_tweets = np.vstack(vectorized_tweets.vector.apply(lambda x: x.tolist()))
    cos=model.cosine_similarities(vectorized_input['vector'].reshape(-1,), vec_tweets)
    vectorized_tweets.loc[:,'similarity_score'] = cos 
    vectorized_tweets = vectorized_tweets.sort_values(by='similarity_score', ascending=False)
    return vectorized_tweets[0:topn]
# --------------------------------------------------------

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
        vectorized_tweets = vectorize_latest_tweets(tweets, model)
        vectorized_user_input = vectorize_user_input(user_input, model)
        #find the top topn= 10  similar tweets
        recommendations = find_most_similar_tweets(vectorized_user_input, vectorized_tweets, topn)
        print('top '+ str(topn) + ' similar tweets are obtained!')
    return recommendations
# ---------------------------------------------------


#downloaded pretrained model
model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary = True)

# -----------------------------------------------------

data_dir = '/Users/shahla/Dropbox/SharpestMinds/stream/data/'
topic = 'Canada' #it can be a list of topics,  comman means 'or'
topn = 10
time_limit = 20
user_input = 'tariff'
with open("/Users/shahla/Dropbox/SharpestMinds/twitter_credentials.json", "r") as file:  
     credentials = json.load(file)
# Instantiate an object
python_tweets = Twython( credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])

# --------------------------------------------------

recommendations = process_user_input(user_input, time_limit, topic, topn)