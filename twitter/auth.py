"""Connects to Twitter API using config.py oauth data"""

from tweepy import OAuthHandler
import config as c


def get_auth():
    auth = OAuthHandler(c.consumer_key, c.consumer_secret)
    auth.set_access_token(c.access_token, c.access_token_secret)
    return auth
    