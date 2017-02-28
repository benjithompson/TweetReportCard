"""holds the tweeter info"""

from collections import defaultdict
from twitter import config as c
from textstat import textstat as ts
from pprint import pprint
import tweepy


def get_api():
    auth = tweepy.OAuthHandler(c.consumer_key, c.consumer_secret)
    auth.set_access_token(c.access_token, c.access_token_secret)
    api = tweepy.API(auth)
    return api

def get_user_dict(nameslist):
    tweeters = defaultdict(Tweeter)
    for name in nameslist:
        user = Tweeter.api.get_user(screen_name=name)
        tweeters[user.name] = Tweeter(user)
    return tweeters

def load_tweets(tweeters):
    for name, tweeter in tweeters.items():
        print('loading tweets from ' + name)
        tweeter.load_tweet_dump(200)

def update_tweeters_stats(tweeters):
    for name, tweeter in tweeters.items():
        tweeter.update_stats()

def print_tweeter_names(tweeters):
    for name, tweeter in tweeters.items():
        print(name + " ID: " + str(tweeter.user.id))

def print_tweeter_tweets(tweeters):
    for name, tweeter in tweeters.items():
        print(name)
        tweeter.print_tweets()

def print_tweeter_stats(tweeters):
    for name, tweeter in tweeters.items():
        print(name)
        tweeter.print_stats()



class Tweeter:

    api = get_api()

    def __init__(self, user):
        self.user = user
        self.name = user.name
        self.screen_name = user.screen_name
        self.tweets = []
        self.stats = Tweeter.init_stats()
        self.tweet_cnt = 0

    @staticmethod
    def init_stats():

        return {
            'flesch_ease': 0,
            'flesch_grade': 0,
            'dalechall': 0,
            'ari': 0,
            'colemanliau': 0,
            'lisear': 0,
            'smog': 0,
            'difcwords': 0,
            'sentences': 0,
            'lexiconcnt': 0,
            'avgsyllables': 0
        }

        #get tweet_dump (max 200 tweets)
    def load_tweet_dump(self, count):
        tweet_dump = Tweeter.api.user_timeline(screen_name=self.screen_name, count=count)
        for tweet in tweet_dump:
            self.tweets.append(tweet.text)
        self.tweet_cnt += len(self.tweets)


    def add_new_tweet(self, msg):
        self.tweets.append(msg)
        self.tweet_cnt += 1

    def update_stats(self):
        tweets_str = ''
        for tweet in self.tweets:
            tweets_str += tweet
        self.stats = Tweeter.get_msg_stats(tweets_str)

    def print_stats(self):
        pprint(self.stats)

    @staticmethod
    def get_msg_stats(msg):
        newstats = {}
        newstats['flesch_ease'] = ts.textstat.flesch_reading_ease(msg)
        newstats['flesch_grade'] = ts.textstat.flesch_kincaid_grade(msg)
        newstats['dalechall'] = ts.textstat.dale_chall_readability_score(msg)
        newstats['ari'] = ts.textstat.automated_readability_index(msg)
        newstats['colemanliau'] = ts.textstat.coleman_liau_index(msg)
        newstats['lisear'] = ts.textstat.linsear_write_formula(msg)
        newstats['smog'] = ts.textstat.smog_index(msg)
        newstats['difcwords'] = ts.textstat.difficult_words(msg)
        newstats['sentences'] = ts.textstat.sentence_count(msg)
        newstats['lexiconcnt'] = ts.textstat.lexicon_count(msg)
        newstats['avgsyllables'] = ts.textstat.avg_syllables_per_word(msg)
        newstats['stdreadability'] = ts.textstat.text_standard(msg)
        return newstats

    def update_stat(self, newmsg):
        new_val = ts.textstat.flesch_reading_ease(newmsg)
        mean = self.stats['flesch_ease']
        num_tweets = len(self.tweets)

        new_mean = mean + ((new_val - mean)/num_tweets)
        #
        #TODO:update all stats

    def print_tweets(self):
        for tweet in self.tweets:
            print(tweet)

