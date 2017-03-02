"""holds the tweeter info"""

from collections import defaultdict
from pprint import pprint
import time
import sys

import tweepy
from textstat import textstat as ts

from twitter import config as c


def get_api():
    """returns tweepy api object"""

    try:
        auth = tweepy.OAuthHandler(c.consumer_key, c.consumer_secret)
        auth.set_access_token(c.access_token, c.access_token_secret)
        api = tweepy.API(auth)
    except tweepy.TweepError as terror:
        print(terror)

    return api

def get_peer_dict(nameslist):
    """returns dict of users objects specified from namelist and returned from api"""

    tweeters = defaultdict(Tweeter)

    for name in nameslist:

        try:
            user = API.get_user(screen_name=name)
        except tweepy.TweepError:
            print(tweepy.TweepError)

        tweeters[user.screen_name] = Tweeter(user)

    return tweeters

def load_tweets(tweeters, cnt):
    """Loads tweets from the API and list of tweeters"""

    for name, tweeter in tweeters.items():
        print('loading tweets from ' + name)
        if cnt <= 0:
            tweeter.load_all_tweets()
        else:
            tweeter.get_tweet_dump(cnt)

def update_tweeters_stats(tweeters):
    """Updates the stats for tweeters in list"""

    for name, tweeter in tweeters.items():
        print('Updating {0} stats...'.format(name))
        tweeter.update_stats()
        print('Update complete.')

def print_tweeter_names(tweeters):
    """prints all tweeter names in dict"""

    for name, tweeter in tweeters.items():
        print(name + " ID: " + str(tweeter.user.id))

def print_tweeter_tweets(tweeters):
    """prints all tweets from tweeters in dict"""

    for name, tweeter in tweeters.items():
        print(name)
        tweeter.print_tweets()

def print_tweeter_stats(tweeters):
    """prints stats from all tweeters in dict"""

    for name, tweeter in tweeters.items():
        print(name)
        tweeter.print_stats()

API = get_api()

def listener(tweeters, wait):
    """checks for new status updates per wait time"""

    pprint('Listening for new tweets...')
    pprint(tweeters)

    while True:
        print('.', end='')
        sys.stdout.flush()
        for name, tweeter in tweeters.items():
            if tweeter.add_new_tweet_msg():
                #get msg stats
                msg_stats = tweeter.get_msg_stats(str(tweeter.get_last_tweet_msg))
                print('Msg Stats: ')
                pprint(msg_stats)
                tweeter.update_stats()
                print('Total Stats: ')
                pprint(tweeter.stats)
            else:
                pass
        time.sleep(wait)

class Tweeter:
    """Holds tweet text and stats as well as common user attributes for easy access"""

    def __init__(self, user):
        self.user = user
        self.name = user.name
        self.screen_name = user.screen_name
        self.user_id = str(user.id)
        self.tweets = []
        self.stats = Tweeter.init_stats()
        self.tweet_cnt = 0
        self.last_status_id = self.get_updated_tweet_id()

    @staticmethod
    def init_stats():
        """initializes all stat fields to 0"""

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

    @staticmethod
    def get_msg_stats(msg):
        """creates new dict and loads it with textstat fields for given msg"""

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

    def load_tweet_dump(self, count):
        """receives tweet text from api and appends to objects tweets list"""

        try:
            tweet_dump = API.user_timeline(screen_name=self.screen_name, count=count)
        except tweepy.TweepError:
            print(tweepy.TweepError)

        for tweet in tweet_dump:
            self.tweets.append(tweet.text)

        self.tweet_cnt += len(self.tweets)

    def load_all_tweets(self):
        """Used from github user yanofsky. Loads all tweets from user"""

        alltweets = []

        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = API.user_timeline(screen_name=self.screen_name, count=200)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print("getting tweets before {0}".format(oldest))

            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = API.user_timeline(screen_name=self.screen_name, count=200, max_id=oldest)

            #save most recent tweets
            alltweets.extend(new_tweets)

            #update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

            print("...{0} tweets downloaded so far".format(len(alltweets)))
        self.tweets.extend(alltweets)

    def get_updated_tweet_id(self):
        """returns the last status id"""
        return str(API.user_timeline(id=self.user_id, count=1)[0].id)

    def get_last_tweet_msg(self):
        """returns the last status msg"""
        last = self.tweets[-1]
        return last

    def add_new_tweet_msg(self):
        """appends msg to objects tweets list if has newer id"""

        new_id = self.get_updated_tweet_id()
        old_id = self.last_status_id

        if new_id > old_id:
            msg = API.user_timeline(id=self.user_id, count=1)[0].text
            self.tweets.append(msg)
            self.tweet_cnt += 1
            self.last_status_id = new_id

            print('\nNew tweet!')
            print('Name: {0}\nOld status: {1}\nNew status: {2}\nMsg: {3}\nNumTweets: {4}'
                  .format(self.name, old_id, new_id, msg, self.tweet_cnt))
            return True
        else:
            return False

    def update_stats(self):
        """trivial way to update stats by concatinating all tweets from tweets list and
           reavaluating stats on entire str"""

        tweets_str = ''
        for tweet in self.tweets:
            tweets_str += tweet.text

        self.stats = Tweeter.get_msg_stats(tweets_str)

    def print_stats(self):
        """prints stats dict using pprint"""

        pprint(self.stats)


    def update_stat(self, newmsg):
        """Incomplete: Optimized way to update numerical stats by updating via single msg
           weight"""

        new_val = ts.textstat.flesch_reading_ease(newmsg)
        mean = self.stats['flesch_ease']
        num_tweets = len(self.tweets)
        new_mean = mean + ((new_val - mean)/num_tweets)
        #TODO:update all stats

    def print_tweets(self):
        """prints all tweets from self tweets list"""

        for tweet in self.tweets:
            print(tweet)
