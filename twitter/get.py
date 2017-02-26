"""Connects to Twitter API using config.py oauth data"""

from tweepy import OAuthHandler
from tweepy import API
import config as c


def auth():
    auth = OAuthHandler(c.consumer_key, c.consumer_secret)
    auth.set_access_token(c.access_token, c.access_token_secret)
    return auth

def user(name):
    return API.get_user(name)
    