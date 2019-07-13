from tweepy import Stream
import pandas as pd
import tweepy
from twython import Twython
from tweepy.streaming import StreamListener
import time
import json


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


def get_latest_tweets(data_dir, auth, time_limit, topic):
    '''
    it gets the latest tweets in time_limit with topic saved in the data_dir
    data_dir: data direcoty
    auth:dddddddd
    '''
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


def get_latest_tweets_for_topic(topic='Canada', data_dir='./', time_limit=20):
    with open(data_dir + "twitter_credentials.json", "r") as file:  
         credentials = json.load(file)
    auth = tweepy.OAuthHandler(credentials['CONSUMER_KEY'], credentials['CONSUMER_SECRET'])
    auth.set_access_token(credentials['ACCESS_TOKEN'], credentials['ACCESS_SECRET'])
    return get_latest_tweets(data_dir, auth, time_limit, topic)


if __name__ == "__main__":
    get_latest_tweets_for_topic()
    
    