"""Connects to Twitter API using config.py oauth data"""

import tweepy
from twitter import config as c

def the_api():
    auth = tweepy.OAuthHandler(c.consumer_key, c.consumer_secret)
    auth.set_access_token(c.access_token, c.access_token_secret)
    api = tweepy.API(auth)
    return api

def the_tweet_dump(api, ):
    tweets = []
    

    