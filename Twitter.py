# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 19:16:13 2018

@author: June

Title: Connecting to twitter API to pull tweets.
"""
#Tweepy lib for connecting to twitter API
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor

#To set schedule.
import schedule
import time
from datetime import datetime

#To create library
import os
import json

#Reading Consumer and Access Keys 
Keys = open("Consumer_Access_Codes.txt", "r").read().split('\n')

consumer_key = Keys[0]
consumer_secret = Keys[1]
access_token = Keys[2]
access_secret = Keys[3]

# Authenticating Tweets API using consumer and access key
class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        return(auth)

# Pulling tweets from timeline.
class TwitterClient():

    def __init__(self, tweeter=None):
        #Authenticating Twitter API.
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        
        #Creating folder to save files.
        dir_path = os.path.dirname(os.path.realpath("Twitter.py"))
        directory = dir_path + '/' + tweeter
        if not os.path.exists(directory):
             os.makedirs(directory)
        
        self.directory = directory

        #Specifying tweeter user.
        self.tweeter = tweeter

    def get_user_timeline_tweets(self, num_tweets):

        #Saving Tweets in a string as a file.
        directory_timeline = self.directory + "/timeline.json"
        f = open(directory_timeline,"a")
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.tweeter).items(num_tweets):
            f.write(json.dumps(tweet._json))

    def get_user_friendlist(self,num_friends):
        #Saving friends in a string as a list.
        directory_timeline = self.directory + "/friends.json"
        f = open(directory_timeline,"a")
        for friend in Cursor(self.twitter_client.friends, id=self.tweeter).items(num_friends):
            f.write(json.dumps(friend._json))

    def get_user_followers(self,num_followers):
        #Saving followers in a string as a list.
        directory_timeline = self.directory + "/followers.json"
        f = open(directory_timeline,"a")
        for follower in Cursor(self.twitter_client.followers, id=self.tweeter).items(num_followers):
            f.write(json.dumps(follower._json))
    
    def get_user_homepage_tweets(self,num_tweets):
        directory_timeline = self.directory + "/homepage.json"
        f = open(directory_timeline,"a")
        for htweet in Cursor(self.twitter_client.home_timeline, id=self.tweeter).items(num_tweets):
            f.write(json.dumps(htweet._json))
        
            
class TweetListener(StreamListener):

    #Simple class that listens to tweets.
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            #Appending tweets to a json file. 
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return(True)
        except BaseException as e:
            #Reading Error as it is.
            print("Error: " + str(e))
            return(True)
    
    def on_error(self, status):
        if status==420:
            #stopping incase it exceeds rates limits
            return(False)
        print(status.text)

class TwitterStreamer():

    def __init__(self):
        #Authenticating Twitter API.
        self.auth = TwitterAuthenticator().authenticate_twitter_app()

    def stream_tweets(self, fetched_filename, hashtags):
        #Authenticating twitter api to listen to tweets.
        listener = TweetListener(fetched_filename)
        stream = Stream(self.auth, listener)

        #Pull Stream of tweets with hashtags.
        stream.filter(track=hashtags)

def collect_donald_tweet():
    print('started! at ' + str(datetime.now()))
    twitter_client = TwitterClient('realDonaldTrump')
    twitter_client.get_user_timeline_tweets(1)
    print('Collected! at ' + str(datetime.now()))


if __name__ == "__main__":

    schedule.every(5).minutes.do(collect_donald_tweet)
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(2)
        except:
            pass

    #hash_tag_list=["donald trump"]
    #fetched_tweets_filename = "tweets.json"

    #twitter_client=TwitterClient('pycon')
    #twitter_client.get_user_timeline_tweets(1)
    #twitter_client.get_user_friendlist(1)
    #twitter_client.get_user_followers(1)

    #twitter_streamer = TwitterStreamer()
    #twitter_streamer.stream_tweets(fetched_tweets_filename,hash_tag_list)
